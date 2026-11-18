"""Initial schema with pgvector extension, documents, extracted_invoices, and validation_logs.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-11-17 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import pgvector.sqlalchemy

# revision identifiers, used by Alembic.
revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _get_existing_indexes(inspector: sa.Inspector, table_name: str, schema: str) -> set[str]:
    return {idx["name"] for idx in inspector.get_indexes(table_name, schema=schema)}


def upgrade() -> None:
    bind = op.get_bind()
    op.execute(sa.text("CREATE EXTENSION IF NOT EXISTS vector"))

    current_schema = bind.execute(sa.text("SELECT current_schema()")).scalar()
    inspector = sa.inspect(bind)

    # 1. documents table
    if not inspector.has_table("documents", schema=current_schema):
        op.create_table(
            "documents",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("filename", sa.String(length=255), nullable=False),
            sa.Column("file_path", sa.String(length=512), nullable=False),
            sa.Column("file_type", sa.String(length=32), nullable=False),
            sa.Column("file_size_bytes", sa.Integer(), nullable=False),
            sa.Column("status", sa.String(length=64), nullable=False),
            sa.Column("error_message", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("file_path"),
        )

    doc_indexes = _get_existing_indexes(inspector, "documents", current_schema)
    if "ix_documents_id" not in doc_indexes:
        op.create_index("ix_documents_id", "documents", ["id"], unique=False)
    if "ix_documents_status" not in doc_indexes:
        op.create_index("ix_documents_status", "documents", ["status"], unique=False)

    # 2. extracted_invoices table
    if not inspector.has_table("extracted_invoices", schema=current_schema):
        op.create_table(
            "extracted_invoices",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("document_id", sa.Integer(), nullable=False),
            sa.Column("invoice_number", sa.String(length=128), nullable=True),
            sa.Column("invoice_date", sa.Date(), nullable=True),
            sa.Column("supplier_name", sa.String(length=255), nullable=True),
            sa.Column("customer_name", sa.String(length=255), nullable=True),
            sa.Column("subtotal", sa.Numeric(precision=12, scale=2), nullable=True),
            sa.Column("tax", sa.Numeric(precision=12, scale=2), nullable=True),
            sa.Column("total_amount", sa.Numeric(precision=12, scale=2), nullable=True),
            sa.Column("currency", sa.String(length=16), nullable=True),
            sa.Column("line_items", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
            sa.Column("is_manually_corrected", sa.Boolean(), nullable=False),
            sa.Column("raw_text", sa.Text(), nullable=True),
            sa.Column("embedding", pgvector.sqlalchemy.Vector(dim=384), nullable=True),
            sa.ForeignKeyConstraint(["document_id"], ["documents.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("document_id"),
        )

    inv_indexes = _get_existing_indexes(inspector, "extracted_invoices", current_schema)
    if "ix_extracted_invoices_id" not in inv_indexes:
        op.create_index("ix_extracted_invoices_id", "extracted_invoices", ["id"], unique=False)
    if "ix_extracted_invoices_invoice_number" not in inv_indexes:
        op.create_index("ix_extracted_invoices_invoice_number", "extracted_invoices", ["invoice_number"], unique=False)
    if "ix_extracted_invoices_supplier_name" not in inv_indexes:
        op.create_index("ix_extracted_invoices_supplier_name", "extracted_invoices", ["supplier_name"], unique=False)
    if "idx_supplier_invoice_num" not in inv_indexes:
        op.create_index("idx_supplier_invoice_num", "extracted_invoices", ["supplier_name", "invoice_number"], unique=False)

    # 3. validation_logs table
    if not inspector.has_table("validation_logs", schema=current_schema):
        op.create_table(
            "validation_logs",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("document_id", sa.Integer(), nullable=False),
            sa.Column("rule_name", sa.String(length=128), nullable=False),
            sa.Column("error_description", sa.Text(), nullable=False),
            sa.Column("severity", sa.String(length=32), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(["document_id"], ["documents.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
        )

    val_indexes = _get_existing_indexes(inspector, "validation_logs", current_schema)
    if "ix_validation_logs_id" not in val_indexes:
        op.create_index("ix_validation_logs_id", "validation_logs", ["id"], unique=False)
    if "ix_validation_logs_document_id" not in val_indexes:
        op.create_index("ix_validation_logs_document_id", "validation_logs", ["document_id"], unique=False)


def downgrade() -> None:
    bind = op.get_bind()
    current_schema = bind.execute(sa.text("SELECT current_schema()")).scalar()
    inspector = sa.inspect(bind)

    if inspector.has_table("validation_logs", schema=current_schema):
        val_indexes = _get_existing_indexes(inspector, "validation_logs", current_schema)
        if "ix_validation_logs_document_id" in val_indexes:
            op.drop_index("ix_validation_logs_document_id", table_name="validation_logs")
        if "ix_validation_logs_id" in val_indexes:
            op.drop_index("ix_validation_logs_id", table_name="validation_logs")
        op.drop_table("validation_logs")

    if inspector.has_table("extracted_invoices", schema=current_schema):
        inv_indexes = _get_existing_indexes(inspector, "extracted_invoices", current_schema)
        if "idx_supplier_invoice_num" in inv_indexes:
            op.drop_index("idx_supplier_invoice_num", table_name="extracted_invoices")
        if "ix_extracted_invoices_supplier_name" in inv_indexes:
            op.drop_index("ix_extracted_invoices_supplier_name", table_name="extracted_invoices")
        if "ix_extracted_invoices_invoice_number" in inv_indexes:
            op.drop_index("ix_extracted_invoices_invoice_number", table_name="extracted_invoices")
        if "ix_extracted_invoices_id" in inv_indexes:
            op.drop_index("ix_extracted_invoices_id", table_name="extracted_invoices")
        op.drop_table("extracted_invoices")

    if inspector.has_table("documents", schema=current_schema):
        doc_indexes = _get_existing_indexes(inspector, "documents", current_schema)
        if "ix_documents_status" in doc_indexes:
            op.drop_index("ix_documents_status", table_name="documents")
        if "ix_documents_id" in doc_indexes:
            op.drop_index("ix_documents_id", table_name="documents")
        op.drop_table("documents")