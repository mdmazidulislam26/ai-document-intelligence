"""Add monotonic lease_epoch fencing token to documents for strict worker fencing.

Revision ID: 0009_lease_epoch_fencing
Revises: 0008_drop_currency_default
Create Date: 2026-11-18 15:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic (must be <= 32 chars).
revision: str = "0009_lease_epoch_fencing"
down_revision: Union[str, None] = "0008_drop_currency_default"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    current_schema = bind.execute(sa.text("SELECT current_schema()")).scalar()
    inspector = sa.inspect(bind)

    existing_cols = {c["name"] for c in inspector.get_columns("documents", schema=current_schema)}
    if "lease_epoch" not in existing_cols:
        op.add_column(
            "documents",
            sa.Column("lease_epoch", sa.Integer(), nullable=False, server_default="0"),
        )


def downgrade() -> None:
    bind = op.get_bind()
    current_schema = bind.execute(sa.text("SELECT current_schema()")).scalar()
    inspector = sa.inspect(bind)

    if inspector.has_table("documents", schema=current_schema):
        existing_cols = {c["name"] for c in inspector.get_columns("documents", schema=current_schema)}
        if "lease_epoch" in existing_cols:
            op.drop_column("documents", "lease_epoch")
