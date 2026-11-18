"""
Automated unit tests for large PDF streaming without page-cap truncation,
OCR preprocessing, typed AI exceptions, and correct line-item merging.
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


def test_large_pdf_no_page_cap_all_pages_retained():
    """Verifies that large PDFs (e.g., 50+ pages) do not drop pages due to an arbitrary 15-page cap."""
    mock_pages = []
    for i in range(1, 31):
        if i == 25:
            mock_pages.append((i, "INVOICE #9900 Total: 450.00 USD Subtotal: 400.00 Tax: 50.00"))
        else:
            mock_pages.append((i, f"Legal standard clause content for page {i}"))

    with patch.object(DocumentParserService, "stream_pdf_pages", return_value=mock_pages):
        text, total_pages = DocumentParserService.extract_full_text("/tmp/mock_large.pdf")
        assert total_pages == 30
        assert "Page 1" in text
        assert "Page 25" in text
        assert "INVOICE #9900" in text
        assert "Page 30" in text


def test_partial_corrupted_page_handling():
    """Ensures a corrupted page does not crash the entire document extraction."""
    mock_pages = [
        (1, "Header and Vendor details"),
        (2, "[Page 2 unreadable due to corruption]"),
        (3, "Total Amount: 500.00 USD")
    ]
    with patch.object(DocumentParserService, "stream_pdf_pages", return_value=mock_pages):
        text, total_pages = DocumentParserService.extract_full_text("/tmp/mock_partial.pdf")
        assert total_pages == 3
        assert "Page 1" in text
        assert "Page 3" in text
        assert "Total Amount: 500.00 USD" in text


def test_legitimate_identical_line_items_preserved():
    """Two legitimate identical line items inside the same document must NOT be dropped."""
    item1 = LineItemSchema(description="Cloud Server", quantity=Decimal("1"), unit_price=Decimal("100.00"), total=Decimal("100.00"))
    item2 = LineItemSchema(description="Cloud Server", quantity=Decimal("1"), unit_price=Decimal("100.00"), total=Decimal("100.00"))

    doc = InvoiceExtractionSchema(
        invoice_number="INV-LEGIT-1",
        subtotal=Decimal("200.00"),
        total_amount=Decimal("200.00"),
        line_items=[item1, item2]
    )

    merged = AIExtractorService.merge_extractions([doc])
    # Both identical items must be preserved (len == 2)
    assert len(merged.line_items) == 2
    assert merged.line_items[0].description == "Cloud Server"
    assert merged.line_items[1].description == "Cloud Server"


def test_chunk_boundary_overlap_duplicate_removed():
    """Only items repeated at the chunk boundary due to chunk overlap should be deduplicated."""
    chunk1 = InvoiceExtractionSchema(
        invoice_number="INV-CHUNKS",
        line_items=[
            LineItemSchema(description="Widget A", quantity=Decimal("1"), unit_price=Decimal("10.00"), total=Decimal("10.00")),
            LineItemSchema(description="Widget B", quantity=Decimal("2"), unit_price=Decimal("20.00"), total=Decimal("40.00")), # Boundary item
        ]
    )
    chunk2 = InvoiceExtractionSchema(
        line_items=[
            LineItemSchema(description="Widget B", quantity=Decimal("2"), unit_price=Decimal("20.00"), total=Decimal("40.00")), # Overlap repeat
            LineItemSchema(description="Widget C", quantity=Decimal("1"), unit_price=Decimal("50.00"), total=Decimal("50.00")), # New item
        ]
    )

    merged = AIExtractorService.merge_extractions([chunk1, chunk2])
    # Total unique items should be 3: Widget A, Widget B, Widget C
    assert len(merged.line_items) == 3
    descriptions = [it.description for it in merged.line_items]
    assert descriptions == ["Widget A", "Widget B", "Widget C"]


def test_different_quantity_same_description_preserved():
    """Items with identical descriptions but different quantities/totals are not duplicates."""
    item1 = LineItemSchema(description="Consulting", quantity=Decimal("5"), unit_price=Decimal("100.00"), total=Decimal("500.00"))
    item2 = LineItemSchema(description="Consulting", quantity=Decimal("2"), unit_price=Decimal("100.00"), total=Decimal("200.00"))

    doc = InvoiceExtractionSchema(
        invoice_number="INV-DIFF-QTY",
        line_items=[item1, item2]
    )
    merged = AIExtractorService.merge_extractions([doc])
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
