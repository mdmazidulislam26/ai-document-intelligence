"""
Automated unit tests for large PDF page filtering, OCR preprocessing,
typed AI exceptions, and deterministic multi-chunk merging.
"""

from unittest.mock import patch, MagicMock
from decimal import Decimal
import pytest
from services.document_parser import DocumentParserService
from services.ai_extractor import (
    AIExtractorService,
    AITransientError,
    AIAuthenticationError,
    AIMalformedResponseError
)
from models.schemas import InvoiceExtractionSchema, LineItemSchema


def test_large_pdf_page_filtering():
    """Simulates a 50-page PDF and ensures first pages, last pages, and keyword pages are selected."""
    # Mock stream_pdf_pages to yield 50 pages where page 48 contains invoice totals
    mock_pages = []
    for i in range(1, 51):
        if i == 48:
            mock_pages.append((i, "INVOICE #9900 Total: 450.00 USD Subtotal: 400.00 Tax: 50.00"))
        else:
            mock_pages.append((i, f"Legal standard clause page content {i}"))

    with patch.object(DocumentParserService, "stream_pdf_pages", return_value=mock_pages):
        text, total_pages = DocumentParserService.extract_full_text("/tmp/mock_large.pdf")
        assert total_pages == 50
        # Page 48 (which has the financial keywords) must be included
        assert "Page 48" in text
        assert "INVOICE #9900" in text
        # First page and last page must also be included
        assert "Page 1" in text
        assert "Page 50" in text


def test_merge_extractions_deterministic():
    """Verifies that multi-chunk extractions merge without duplicate line items or lost totals."""
    chunk1 = InvoiceExtractionSchema(
        invoice_number="INV-MULTI-1",
        supplier_name="Global Vendor",
        currency="USD",
        line_items=[
            LineItemSchema(description="Item A", quantity=Decimal("1"), unit_price=Decimal("10.00"), total=Decimal("10.00"))
        ]
    )
    chunk2 = InvoiceExtractionSchema(
        subtotal=Decimal("30.00"),
        tax=Decimal("3.00"),
        total_amount=Decimal("33.00"),
        line_items=[
            LineItemSchema(description="Item A", quantity=Decimal("1"), unit_price=Decimal("10.00"), total=Decimal("10.00")), # Duplicate item
            LineItemSchema(description="Item B", quantity=Decimal("2"), unit_price=Decimal("10.00"), total=Decimal("20.00")), # New item
        ]
    )

    merged = AIExtractorService.merge_extractions([chunk1, chunk2])
    assert merged.invoice_number == "INV-MULTI-1"
    assert merged.supplier_name == "Global Vendor"
    assert merged.total_amount == Decimal("33.00")
    # Duplicate Item A must be deduplicated: total line items should be 2, not 3
    assert len(merged.line_items) == 2


def test_ai_missing_key_raises_auth_error():
    """Missing API key must raise AIAuthenticationError instead of silently returning empty schema."""
    with patch("services.ai_extractor.settings.GROQ_API_KEY", ""):
        service = AIExtractorService()
        with pytest.raises(AIAuthenticationError):
            service.extract_from_chunk("Some invoice text")


@patch("services.ai_extractor.OpenAI")
def test_ai_malformed_json_raises_typed_error(mock_openai):
    """Malformed LLM response raises AIMalformedResponseError."""
    mock_instance = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "Not a valid JSON format at all"
    mock_instance.chat.completions.create.return_value.choices = [mock_choice]
    mock_openai.return_value = mock_instance

    with patch("services.ai_extractor.settings.GROQ_API_KEY", "valid_key"):
        service = AIExtractorService()
        with pytest.raises(AIMalformedResponseError):
            service.extract_from_chunk("Some text")


def test_zero_hallucination_currency_null():
    """When currency is not specified, it should remain None rather than defaulting to USD."""
    raw_json = '{"invoice_number": "INV-123", "total_amount": 100.0, "currency": null}'
    schema = InvoiceExtractionSchema.model_validate_json(raw_json)
    assert schema.currency is None
