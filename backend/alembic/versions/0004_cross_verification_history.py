"""Add cross_verification_history table for PDF-to-PDF and PDF-to-Spreadsheet verification logs.

Revision ID: 0004_cross_verify_history
Revises: 0003_hybrid_search_indexes
Create Date: 2026-11-17 00:15:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic (must be <= 32 chars).
revision: str = "0004_cross_verify_history"
down_revision: Union[str, None] = "0003_hybrid_search_indexes"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _get_existing_indexes(inspector: sa.Inspector, table_name: str, schema: str) -> set[str]:
    return {idx["name"] for idx in inspector.get_indexes(table_name, schema=schema)}


def upgrade() -> None:
    bind = op.get_bind()
    current_schema = bind.execute(sa.text("SELECT current_schema()")).scalar()
    inspector = sa.inspect(bind)

    if not inspector.has_table("cross_verification_history", schema=current_schema):
        op.create_table(
            "cross_verification_history",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("document_id", sa.Integer(), nullable=False),
            sa.Column("reference_document_id", sa.Integer(), nullable=False),
            sa.Column("verification_mode", sa.String(length=64), nullable=False),
            sa.Column("overall_status", sa.String(length=64), nullable=False),
            sa.Column("discrepancy_count", sa.Integer(), nullable=False),
            sa.Column("comparison_details", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(["document_id"], ["documents.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["reference_document_id"], ["documents.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
        )

    existing_indexes = _get_existing_indexes(inspector, "cross_verification_history", current_schema)
    if "ix_cross_verification_history_id" not in existing_indexes:
        op.create_index("ix_cross_verification_history_id", "cross_verification_history", ["id"], unique=False)
    if "ix_cross_verification_history_document_id" not in existing_indexes:
        op.create_index("ix_cross_verification_history_document_id", "cross_verification_history", ["document_id"], unique=False)
    if "ix_cross_verification_history_reference_document_id" not in existing_indexes:
        op.create_index(
            "ix_cross_verification_history_reference_document_id",
            "cross_verification_history",
            ["reference_document_id"],
            unique=False,
        )


def downgrade() -> None:
    bind = op.get_bind()
    current_schema = bind.execute(sa.text("SELECT current_schema()")).scalar()
    inspector = sa.inspect(bind)

    if inspector.has_table("cross_verification_history", schema=current_schema):
        existing_indexes = _get_existing_indexes(inspector, "cross_verification_history", current_schema)
        for idx_name in [
            "ix_cross_verification_history_reference_document_id",
            "ix_cross_verification_history_document_id",
            "ix_cross_verification_history_id",
        ]:
            if idx_name in existing_indexes:
                op.drop_index(idx_name, table_name="cross_verification_history")
        op.drop_table("cross_verification_history")
