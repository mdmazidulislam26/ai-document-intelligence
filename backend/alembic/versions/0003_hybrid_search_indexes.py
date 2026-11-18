"""Add stored tsvector search_vector, GIN FTS index, pgvector HNSW index, and lower() lookup indexes.

Revision ID: 0003_hybrid_search_indexes
Revises: 0002_financial_precision
Create Date: 2026-11-17 00:10:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic (must be <= 32 chars).
revision: str = "0003_hybrid_search_indexes"
down_revision: Union[str, None] = "0002_financial_precision"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _get_existing_indexes(inspector: sa.Inspector, table_name: str, schema: str) -> set[str]:
    return {idx["name"] for idx in inspector.get_indexes(table_name, schema=schema)}


def upgrade() -> None:
    bind = op.get_bind()
    current_schema = bind.execute(sa.text("SELECT current_schema()")).scalar()
    inspector = sa.inspect(bind)

    existing_cols = {c["name"] for c in inspector.get_columns("extracted_invoices", schema=current_schema)}

    # 1. Stored generated tsvector column (auto-populates existing rows on creation)
    if "search_vector" not in existing_cols:
        op.execute(
            sa.text("""
                ALTER TABLE extracted_invoices
                ADD COLUMN search_vector tsvector
                GENERATED ALWAYS AS (
                    to_tsvector(
                        'english',
                        coalesce(supplier_name, '') || ' ' ||
                        coalesce(invoice_number, '') || ' ' ||
                        coalesce(customer_name, '') || ' ' ||
                        coalesce(raw_text, '')
                    )
                ) STORED
            """)
        )

    existing_indexes = _get_existing_indexes(inspector, "extracted_invoices", current_schema)

    # 2. GIN index on stored tsvector column
    if "idx_extracted_invoices_search_vector" not in existing_indexes:
        op.execute(
            sa.text("""
                CREATE INDEX idx_extracted_invoices_search_vector
                ON extracted_invoices
                USING gin (search_vector)
            """)
        )

    # 3. pgvector HNSW index for cosine distance (<=>)
    if "idx_extracted_invoices_embedding_hnsw" not in existing_indexes:
        op.execute(
            sa.text("""
                CREATE INDEX idx_extracted_invoices_embedding_hnsw
                ON extracted_invoices
                USING hnsw (embedding vector_cosine_ops)
                WITH (m = 16, ef_construction = 64)
            """)
        )

    # 4. Expression B-tree indexes for exact case-insensitive identifier matching
    if "idx_extracted_invoices_inv_lower" not in existing_indexes:
        op.execute(
            sa.text("""
                CREATE INDEX idx_extracted_invoices_inv_lower
                ON extracted_invoices (LOWER(invoice_number))
            """)
        )

    if "idx_extracted_invoices_sup_lower" not in existing_indexes:
        op.execute(
            sa.text("""
                CREATE INDEX idx_extracted_invoices_sup_lower
                ON extracted_invoices (LOWER(supplier_name))
            """)
        )


def downgrade() -> None:
    bind = op.get_bind()
    current_schema = bind.execute(sa.text("SELECT current_schema()")).scalar()
    inspector = sa.inspect(bind)

    if not inspector.has_table("extracted_invoices", schema=current_schema):
        return

    existing_indexes = _get_existing_indexes(inspector, "extracted_invoices", current_schema)

    for idx_name in [
        "idx_extracted_invoices_sup_lower",
        "idx_extracted_invoices_inv_lower",
        "idx_extracted_invoices_embedding_hnsw",
        "idx_extracted_invoices_search_vector",
    ]:
        if idx_name in existing_indexes:
            op.execute(sa.text(f"DROP INDEX IF EXISTS {idx_name}"))

    existing_cols = {c["name"] for c in inspector.get_columns("extracted_invoices", schema=current_schema)}
    if "search_vector" in existing_cols:
        op.drop_column("extracted_invoices", "search_vector")
