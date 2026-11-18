"""
Pydantic v2 validation schemas for API requests, responses, AI structured output,
rich hybrid search results, and cross-document verification.
Preserves exact Decimal precision and unknown (null) currency.
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


def _normalize_currency(val: Any) -> Optional[str]:
    if val is None:
        return None
    cleaned = str(val).strip()
    if not cleaned or cleaned.lower() in ("null", "none", "unknown", "n/a"):
        return None
    return cleaned.upper()


class LineItemSchema(BaseModel):
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

    @field_validator("currency", mode="before")
    @classmethod
    def parse_currency(cls, v: Any) -> Optional[str]:
        return _normalize_currency(v)


class ValidationLogSchema(BaseModel):
    rule_name: str
    error_description: str
    severity: str

    model_config = ConfigDict(from_attributes=True)


class ExtractedInvoiceResponse(BaseModel):
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
    id: int
    filename: str
    status: str
    error_message: Optional[str]


class ManualCorrectionRequest(BaseModel):
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

    @field_validator("currency", mode="before")
    @classmethod
    def parse_currency(cls, v: Any) -> Optional[str]:
        return _normalize_currency(v)


class CrossVerifyRequest(BaseModel):
    reference_document_id: int = Field(..., ge=1, description="ID of the reference PDF, image, Excel, or CSV document")


class CrossVerificationResponse(BaseModel):
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
    query: str
    search_type: str = Field(default="hybrid", description="keyword | semantic | hybrid")
    limit: int = Field(default=10, ge=1, le=50)


class SearchResultItem(BaseModel):
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
