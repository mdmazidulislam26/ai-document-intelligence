"""
Pydantic v2 validation schemas for API requests, responses, and AI structured output.
"""

from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


# ---------------------------------------------------------
# AI Extraction Schemas (Enforces Zero-Hallucination Policy)
# ---------------------------------------------------------

class LineItemSchema(BaseModel):
    """Represents an individual itemized line in an invoice."""
    description: Optional[str] = Field(default=None, description="Item description or name")
    quantity: Optional[float] = Field(default=None, description="Quantity purchased")
    unit_price: Optional[float] = Field(default=None, description="Price per individual unit")
    total: Optional[float] = Field(default=None, description="Total amount for this specific line item")


class InvoiceExtractionSchema(BaseModel):
    """
    Schema passed to the LLM for structured output.
    Any missing or unreadable field must resolve to None.
    """
    invoice_number: Optional[str] = Field(default=None, description="Official invoice identifier or reference code")
    invoice_date: Optional[str] = Field(default=None, description="Issue date in YYYY-MM-DD string format if discernable")
    supplier_name: Optional[str] = Field(default=None, description="Name of the billing vendor, supplier, or company")
    customer_name: Optional[str] = Field(default=None, description="Name of the billed client, company, or customer")
    subtotal: Optional[float] = Field(default=None, description="Taxable amount before tax/shipping")
    tax: Optional[float] = Field(default=None, description="Total sales tax, VAT, or GST applied")
    total_amount: Optional[float] = Field(default=None, description="Final gross total payable amount")
    currency: Optional[str] = Field(default="USD", description="3-letter ISO currency code or currency symbol")
    line_items: List[LineItemSchema] = Field(default_factory=list, description="List of itemized products or services")


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
    subtotal: Optional[float]
    tax: Optional[float]
    total_amount: Optional[float]
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
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: Optional[List[dict]] = None


class SearchRequest(BaseModel):
    """Request model for document search endpoint."""
    query: str
    search_type: str = Field(default="hybrid", description="keyword | semantic | hybrid")
    limit: int = Field(default=10, ge=1, le=50)


class SearchResultItem(BaseModel):
    """Single item returned in search queries."""
    document_id: int
    filename: str
    supplier_name: Optional[str]
    invoice_number: Optional[str]
    total_amount: Optional[float]
    status: str
    similarity_score: Optional[float] = None