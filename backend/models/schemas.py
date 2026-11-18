"""
Pydantic v2 validation schemas for API requests, responses, AI structured output,
rich hybrid search results, and cross-document verification.
Preserves exact Decimal precision without binary float intermediate artifacts.
"""

import re
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator


def _coerce_decimal(val: Any) -> Optional[Decimal]:
    if val is None or val == "":
        return None
    if isinstance(val, Decimal):
        return val
    if isinstance(val, bool):
        return None
    if isinstance(val, int):
        return Decimal(val)
    if isinstance(val, float):
        return Decimal(str(val))
    if isinstance(val, str):
        cleaned = re.sub(r"[^\d.-]", "", val.strip())
        if not cleaned or cleaned == "-":
            return None
        return Decimal(cleaned)
    return Decimal(str(val))


# ---------------------------------------------------------
# AI Extraction Schemas (Enforces Zero-Hallucination Policy)
# ---------------------------------------------------------

class LineItemSchema(BaseModel):
    """Represents an individual itemized line in an invoice."""
    description: Optional[str] = Field(default=None, description="Item description or name")
    quantity: Optional[Decimal] = Field(default=None, description="Quantity purchased")
    unit_price: Optional[Decimal] = Field(default=None, description="Price per individual unit")
    total: Optional[Decimal] = Field(default=None, description="Total amount for this specific line item")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("quantity", "unit_price", "total", mode="before")
    @classmethod
    def parse_decimal_fields(cls, v: Any) -> Optional[Decimal]:
        return _coerce_decimal(v)


class InvoiceExtractionSchema(BaseModel):
    """
    Schema passed to the LLM for structured output.
    Any missing or unreadable field must resolve to None.
    """
    invoice_number: Optional[str] = Field(default=None, description="Official invoice identifier or reference code")
    invoice_date: Optional[str] = Field(default=None, description="Issue date in YYYY-MM-DD string format if discernable")
    supplier_name: Optional[str] = Field(default=None, description="Name of the billing vendor, supplier, or company")
    customer_name: Optional[str] = Field(default=None, description="Name of the billed client, company, or customer")
    subtotal: Optional[Decimal] = Field(default=None, description="Taxable amount before tax/shipping")
    tax: Optional[Decimal] = Field(default=None, description="Total sales tax, VAT, or GST applied")
    total_amount: Optional[Decimal] = Field(default=None, description="Final gross total payable amount")
    currency: Optional[str] = Field(default=None, description="3-letter ISO currency code or currency symbol")
    line_items: List[LineItemSchema] = Field(default_factory=list, description="List of itemized products or services")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("subtotal", "tax", "total_amount", mode="before")
    @classmethod
    def parse_monetary_fields(cls, v: Any) -> Optional[Decimal]:
        return _coerce_decimal(v)


# ---------------------------------------------------------
# API Response & Request Schemas
# ---------------------------------------------------------

class ValidationLogSchema(BaseModel):
    """Validation failure detail model."""
    rule_name: str
    error_description: str
    severity: str

    model_config = ConfigDict(from_attributes=True)


class ExtractedInvoiceResponse(BaseModel):
    """Structured invoice response returned to the client."""
    id: int
    document_id: int
    invoice_number: Optional[str]
    invoice_date: Optional[date]
    supplier_name: Optional[str]
    customer_name: Optional[str]
    subtotal: Optional[Decimal]
    tax: Optional[Decimal]
    total_amount: Optional[Decimal]
    currency: Optional[str]
    line_items: List[dict]
    is_manually_corrected: bool

    model_config = ConfigDict(from_attributes=True)


class DocumentResponse(BaseModel):
    """Detailed document status and extracted content."""
    id: int
    filename: str
    file_type: str
    file_size_bytes: int
    status: str
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime
    extracted_invoice: Optional[ExtractedInvoiceResponse] = None
    validation_logs: List[ValidationLogSchema] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class DocumentStatusResponse(BaseModel):
    """Lightweight response for polling processing progress."""
    id: int
    filename: str
    status: str
    error_message: Optional[str]


class ManualCorrectionRequest(BaseModel):
    """Payload submitted when a user manually reviews and corrects invoice values."""
    invoice_number: Optional[str] = None
    invoice_date: Optional[date] = None
    supplier_name: Optional[str] = None
    customer_name: Optional[str] = None
    subtotal: Optional[Decimal] = None
    tax: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    currency: Optional[str] = None
    line_items: Optional[List[dict]] = None

    @field_validator("subtotal", "tax", "total_amount", mode="before")
    @classmethod
    def parse_monetary_fields(cls, v: Any) -> Optional[Decimal]:
        return _coerce_decimal(v)


class CrossVerifyRequest(BaseModel):
    """Request payload to cross-verify a processed document against a reference document."""
    reference_document_id: int = Field(..., ge=1, description="ID of the reference PDF, image, Excel, or CSV document")


class CrossVerificationResponse(BaseModel):
    """Structured response for cross-document verification."""
    id: int
    document_id: int
    reference_document_id: int
    verification_mode: str
    overall_status: str
    discrepancy_count: int
    comparison_details: Dict[str, Any]
    validation_logs: List[ValidationLogSchema] = Field(default_factory=list)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SearchRequest(BaseModel):
    """Request model for document search endpoint."""
    query: str
    search_type: str = Field(default="hybrid", description="keyword | semantic | hybrid")
    limit: int = Field(default=10, ge=1, le=50)


class SearchResultItem(BaseModel):
    """Single item returned in search queries with rich ranking metadata."""
    document_id: int
    filename: str
    supplier_name: Optional[str] = None
    invoice_number: Optional[str] = None
    total_amount: Optional[Decimal] = None
    currency: Optional[str] = None
    status: str
    similarity_score: Optional[float] = None
    rrf_score: Optional[float] = None
    match_type: Optional[str] = Field(default="hybrid", description="hybrid | keyword_only | semantic_only")
    keyword_rank: Optional[int] = None
    semantic_rank: Optional[int] = None
