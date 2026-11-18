"""Safely migrate legacy float/timestamp columns to Numeric(12, 2) and Date without data loss.

Revision ID: 0002_financial_precision
Revises: 0001_initial_schema
Create Date: 2026-11-17 00:05:00.000000
"""

from typing import Sequence, Union, Dict, Any

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic (must be <= 32 chars).
revision: str = "0002_financial_precision"
down_revision: Union[str, None] = "0001_initial_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _get_column_info(bind, table_name: str) -> Dict[str, Dict[str, Any]]:
    rows = bind.execute(
        sa.text("""
            SELECT column_name, data_type, numeric_precision, numeric_scale
            FROM information_schema.columns
            WHERE table_schema = current_schema()
              AND table_name = :table_name
        """),
        {"table_name": table_name},
    ).mappings()
    return {r["column_name"]: dict(r) for r in rows}


def upgrade() -> None:
    bind = op.get_bind()
    cols = _get_column_info(bind, "extracted_invoices")

    # Safely convert monetary columns to NUMERIC(12, 2) preserving existing rows
    for col_name in ["subtotal", "tax", "total_amount"]:
        col_meta = cols.get(col_name)
        if not col_meta:
            continue
        is_already_numeric_12_2 = (
            col_meta["data_type"] == "numeric"
            and col_meta["numeric_precision"] == 12
            and col_meta["numeric_scale"] == 2
        )
        if not is_already_numeric_12_2:
            op.execute(
                sa.text(f"""
                    ALTER TABLE extracted_invoices
                    ALTER COLUMN {col_name} TYPE NUMERIC(12, 2)
                    USING CASE
                        WHEN {col_name} IS NULL THEN NULL
                        WHEN {col_name}::text IN ('NaN', 'Infinity', '-Infinity') THEN NULL
                        ELSE ROUND({col_name}::numeric, 2)
                    END
                """)
            )

    # Safely convert invoice_date to DATE preserving existing rows
    date_meta = cols.get("invoice_date")
    if date_meta and date_meta["data_type"] != "date":
        if date_meta["data_type"] in ("character varying", "text"):
            op.execute(
                sa.text("""
                    ALTER TABLE extracted_invoices
                    ALTER COLUMN invoice_date TYPE DATE
                    USING CASE
                        WHEN NULLIF(TRIM(invoice_date::text), '') IS NULL THEN NULL
                        ELSE invoice_date::date
                    END
                """)
            )
        else:
            op.execute(
                sa.text("""
                    ALTER TABLE extracted_invoices
                    ALTER COLUMN invoice_date TYPE DATE
                    USING CASE
                        WHEN invoice_date IS NULL THEN NULL
                        ELSE invoice_date::date
                    END
                """)
            )


def downgrade() -> None:
    bind = op.get_bind()
    cols = _get_column_info(bind, "extracted_invoices")

    # Non-destructive downgrade back to DOUBLE PRECISION and TIMESTAMP
    for col_name in ["subtotal", "tax", "total_amount"]:
        col_meta = cols.get(col_name)
        if col_meta and col_meta["data_type"] == "numeric":
            op.execute(
                sa.text(f"""
                    ALTER TABLE extracted_invoices
                    ALTER COLUMN {col_name} TYPE DOUBLE PRECISION
                    USING {col_name}::double precision
                """)
            )

    date_meta = cols.get("invoice_date")
    if date_meta and date_meta["data_type"] == "date":
        op.execute(
            sa.text("""
                ALTER TABLE extracted_invoices
                ALTER COLUMN invoice_date TYPE TIMESTAMP WITHOUT TIME ZONE
                USING invoice_date::timestamp
            """)
        )