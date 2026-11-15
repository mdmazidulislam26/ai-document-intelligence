"""
SQLAlchemy ORM models defining documents, extracted invoice data, and validation logs.
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    Index
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from core.database import Base
from core.config import settings


class Document(Base):
    """
    Stores original uploaded file metadata, execution lifecycle, and error logs.
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False, unique=True)
    file_type = Column(String(32), nullable=False)
    file_size_bytes = Column(Integer, nullable=False, default=0)
    
    # Possible statuses: queued, processing, validated, requires_manual_review, failed
    status = Column(String(64), nullable=False, default="queued", index=True)
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
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


class ExtractedInvoice(Base):
    """
    Stores structured financial records extracted from documents,
    along with pgvector dense vector embeddings for semantic search.
    """
    __tablename__ = "extracted_invoices"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    invoice_number = Column(String(128), nullable=True, index=True)
    invoice_date = Column(DateTime, nullable=True)
    supplier_name = Column(String(255), nullable=True, index=True)
    customer_name = Column(String(255), nullable=True)
    
    subtotal = Column(Float, nullable=True)
    tax = Column(Float, nullable=True)
    total_amount = Column(Float, nullable=True)
    currency = Column(String(16), nullable=True, default="USD")
    
    # Itemized lines stored as JSON array of objects
    line_items = Column(JSONB, nullable=False, default=list)
    
    # Flags whether human in the loop performed manual correction
    is_manually_corrected = Column(Boolean, default=False, nullable=False)
    raw_text = Column(Text, nullable=True)

    # pgvector embedding: 384 dimensions matching local FastEmbed model
    embedding = Column(Vector(settings.EMBEDDING_DIMENSION), nullable=True)

    # Relationship
    document = relationship("Document", back_populates="extracted_invoice")

    # Composite index to rapidly identify duplicate invoices
    __table_args__ = (
        Index("idx_supplier_invoice_num", "supplier_name", "invoice_number"),
    )


class ValidationLog(Base):
    """
    Stores reconciliation and format validation results per document.
    """
    __tablename__ = "validation_logs"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    
    rule_name = Column(String(128), nullable=False)
    error_description = Column(Text, nullable=False)
    severity = Column(String(32), nullable=False, default="WARNING")  # WARNING, ERROR, CRITICAL
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    document = relationship("Document", back_populates="validation_logs")