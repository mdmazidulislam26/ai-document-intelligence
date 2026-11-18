"""
SQLAlchemy ORM models defining documents, extracted invoice data, validation logs,
cross-document verification history, and transactional task outbox.
Includes owner_id scoping on Document to prevent unauthorized cross-tenant access.
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Date,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    Index,
    Computed,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from core.database import Base
from core.config import settings


class Document(Base):
    """
    Stores original uploaded file metadata, ownership scope, execution lifecycle, and error logs.
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(String(128), nullable=False, default="default", server_default="default", index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False, unique=True)
    file_type = Column(String(32), nullable=False)
    file_size_bytes = Column(Integer, nullable=False, default=0)

    status = Column(String(64), nullable=False, default="queued", index=True)
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    extracted_invoice = relationship(
        "ExtractedInvoice",
        back_populates="document",
        uselist=False,
        cascade="all, delete-orphan"
    )
    validation_logs = relationship(
        "ValidationLog",
        back_populates="document",
        cascade="all, delete-orphan"
    )
    cross_verifications = relationship(
        "CrossVerificationHistory",
        foreign_keys="CrossVerificationHistory.document_id",
        back_populates="document",
        cascade="all, delete-orphan"
    )
    outbox_entries = relationship(
        "TaskOutbox",
        back_populates="document",
        cascade="all, delete-orphan"
    )


class ExtractedInvoice(Base):
    """Stores structured financial records extracted from documents."""
    __tablename__ = "extracted_invoices"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, unique=True)

    invoice_number = Column(String(128), nullable=True, index=True)
    invoice_date = Column(Date, nullable=True)
    supplier_name = Column(String(255), nullable=True, index=True)
    customer_name = Column(String(255), nullable=True)

    subtotal = Column(Numeric(12, 2), nullable=True)
    tax = Column(Numeric(12, 2), nullable=True)
    total_amount = Column(Numeric(12, 2), nullable=True)
    currency = Column(String(16), nullable=True, default="USD")

    line_items = Column(JSONB, nullable=False, default=list)
    is_manually_corrected = Column(Boolean, default=False, nullable=False)
    raw_text = Column(Text, nullable=True)

    search_vector = Column(
        TSVECTOR,
        Computed(
            "to_tsvector('english', coalesce(supplier_name, '') || ' ' || "
            "coalesce(invoice_number, '') || ' ' || "
            "coalesce(customer_name, '') || ' ' || "
            "coalesce(raw_text, ''))",
            persisted=True,
        ),
        nullable=True,
    )

    embedding = Column(Vector(settings.EMBEDDING_DIMENSION), nullable=True)

    document = relationship("Document", back_populates="extracted_invoice")

    __table_args__ = (
        Index("idx_supplier_invoice_num", "supplier_name", "invoice_number"),
        Index("idx_extracted_invoices_search_vector", "search_vector", postgresql_using="gin"),
        Index(
            "idx_extracted_invoices_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
        Index("idx_extracted_invoices_inv_lower", func.lower(invoice_number)),
        Index("idx_extracted_invoices_sup_lower", func.lower(supplier_name)),
    )


class ValidationLog(Base):
    """Stores reconciliation and format validation results per document."""
    __tablename__ = "validation_logs"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)

    rule_name = Column(String(128), nullable=False)
    error_description = Column(Text, nullable=False)
    severity = Column(String(32), nullable=False, default="WARNING")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    document = relationship("Document", back_populates="validation_logs")


class CrossVerificationHistory(Base):
    """Stores persistent audit history of PDF-to-PDF and PDF-to-Spreadsheet cross-verifications."""
    __tablename__ = "cross_verification_history"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    reference_document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)

    verification_mode = Column(String(64), nullable=False)
    overall_status = Column(String(64), nullable=False)
    discrepancy_count = Column(Integer, nullable=False, default=0)
    comparison_details = Column(JSONB, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    document = relationship("Document", foreign_keys=[document_id], back_populates="cross_verifications")
    reference_document = relationship("Document", foreign_keys=[reference_document_id])


class TaskOutbox(Base):
    """Transactional outbox for reliable Celery task dispatch across Redis/broker outages."""
    __tablename__ = "task_outbox"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    task_name = Column(String(128), nullable=False, default="tasks.processing_tasks.process_document_task")
    status = Column(String(32), nullable=False, default="pending", index=True)
    attempts = Column(Integer, nullable=False, default=0)
    last_error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    dispatched_at = Column(DateTime, nullable=True)
    next_attempt_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    document = relationship("Document", back_populates="outbox_entries")

    __table_args__ = (
        Index("idx_task_outbox_pending_next", "status", "next_attempt_at"),
    )
