"""Ensure extracted_invoices.currency has no database-level default (preserve null).

Revision ID: 0008_drop_currency_default
Revises: 0007_worker_lease_currency
Create Date: 2026-11-18 00:10:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic (must be <= 32 chars).
revision: str = "0008_drop_currency_default"
down_revision: Union[str, None] = "0007_worker_lease_currency"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.text("ALTER TABLE extracted_invoices ALTER COLUMN currency DROP DEFAULT"))


def downgrade() -> None:
    # No-op: preserving nullable currency without re-introducing default 'USD'
    pass
