"""Add owner_id column and index to documents for tenant/owner access control.

Revision ID: 0006_security_owner_scope
Revises: 0005_task_outbox
Create Date: 2026-11-17 00:35:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic (must be <= 32 chars).
revision: str = "0006_security_owner_scope"
down_revision: Union[str, None] = "0005_task_outbox"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _get_existing_indexes(inspector: sa.Inspector, table_name: str, schema: str) -> set[str]:
    return {idx["name"] for idx in inspector.get_indexes(table_name, schema=schema)}


def upgrade() -> None:
    bind = op.get_bind()
    current_schema = bind.execute(sa.text("SELECT current_schema()")).scalar()
    inspector = sa.inspect(bind)

    existing_cols = {c["name"] for c in inspector.get_columns("documents", schema=current_schema)}
    if "owner_id" not in existing_cols:
        op.add_column(
            "documents",
            sa.Column("owner_id", sa.String(length=128), nullable=False, server_default="default"),
        )

    existing_indexes = _get_existing_indexes(inspector, "documents", current_schema)
    if "ix_documents_owner_id" not in existing_indexes:
        op.create_index("ix_documents_owner_id", "documents", ["owner_id"], unique=False)


def downgrade() -> None:
    bind = op.get_bind()
    current_schema = bind.execute(sa.text("SELECT current_schema()")).scalar()
    inspector = sa.inspect(bind)

    if inspector.has_table("documents", schema=current_schema):
        existing_indexes = _get_existing_indexes(inspector, "documents", current_schema)
        if "ix_documents_owner_id" in existing_indexes:
            op.drop_index("ix_documents_owner_id", table_name="documents")

        existing_cols = {c["name"] for c in inspector.get_columns("documents", schema=current_schema)}
        if "owner_id" in existing_cols:
            op.drop_column("documents", "owner_id")
