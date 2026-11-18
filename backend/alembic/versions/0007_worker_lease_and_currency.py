"""Add worker_id, processing_lease_until, and last_heartbeat_at columns to documents.

Revision ID: 0007_worker_lease_currency
Revises: 0006_security_owner_scope
Create Date: 2026-11-18 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic (must be <= 32 chars).
revision: str = "0007_worker_lease_currency"
down_revision: Union[str, None] = "0006_security_owner_scope"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _get_existing_indexes(inspector: sa.Inspector, table_name: str, schema: str) -> set[str]:
    return {idx["name"] for idx in inspector.get_indexes(table_name, schema=schema)}


def upgrade() -> None:
    bind = op.get_bind()
    current_schema = bind.execute(sa.text("SELECT current_schema()")).scalar()
    inspector = sa.inspect(bind)

    existing_cols = {c["name"] for c in inspector.get_columns("documents", schema=current_schema)}

    if "worker_id" not in existing_cols:
        op.add_column("documents", sa.Column("worker_id", sa.String(length=128), nullable=True))
    if "processing_lease_until" not in existing_cols:
        op.add_column("documents", sa.Column("processing_lease_until", sa.DateTime(), nullable=True))
    if "last_heartbeat_at" not in existing_cols:
        op.add_column("documents", sa.Column("last_heartbeat_at", sa.DateTime(), nullable=True))

    existing_indexes = _get_existing_indexes(inspector, "documents", current_schema)
    if "ix_documents_processing_lease_until" not in existing_indexes:
        op.create_index(
            "ix_documents_processing_lease_until",
            "documents",
            ["processing_lease_until"],
            unique=False,
        )


def downgrade() -> None:
    bind = op.get_bind()
    current_schema = bind.execute(sa.text("SELECT current_schema()")).scalar()
    inspector = sa.inspect(bind)

    if inspector.has_table("documents", schema=current_schema):
        existing_indexes = _get_existing_indexes(inspector, "documents", current_schema)
        if "ix_documents_processing_lease_until" in existing_indexes:
            op.drop_index("ix_documents_processing_lease_until", table_name="documents")

        existing_cols = {c["name"] for c in inspector.get_columns("documents", schema=current_schema)}
        for col_name in ("last_heartbeat_at", "processing_lease_until", "worker_id"):
            if col_name in existing_cols:
                op.drop_column("documents", col_name)
