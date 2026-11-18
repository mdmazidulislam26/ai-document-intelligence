"""
Tests verifying Decimal financial precision across AI extraction, JSONB storage,
manual correction API serialization, PostgreSQL persistence, and xlrd availability.
"""

import json
import uuid
from decimal import Decimal
from datetime import date
from unittest.mock import patch, MagicMock
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from core.config import settings
from core.database import get_db
from main import app
from services.validator import DocumentValidator, normalize_line_items_for_jsonb
from services.ai_extractor import AIExtractorService
from models.schemas import InvoiceExtractionSchema, LineItemSchema
from models.document import ExtractedInvoice

DEV_HEADERS = {"X-API-Key": "dev-local-api-key-change-me"}


def test_decimal_subtotal_tax_addition_precision():
    data = InvoiceExtractionSchema(
        invoice_number="INV-DECIMAL-1",
        invoice_date="2024-05-01",
        subtotal=Decimal("100.10"),
        tax=Decimal("20.20"),
        total_amount=Decimal("120.30"),
        line_items=[
            LineItemSchema(description="Item 1", quantity=Decimal("1"), unit_price=Decimal("100.10"), total=Decimal("100.10"))
        ]
    )
    assert len(DocumentValidator.validate_math(data)) == 0


def test_floating_point_rounding_discrepancy_prevention():
    data = InvoiceExtractionSchema(
        invoice_number="INV-PRECISION-2",
        invoice_date="2024-05-01",
        subtotal=Decimal("0.10"),
        tax=Decimal("0.20"),
        total_amount=Decimal("0.30"),
        line_items=[
            LineItemSchema(description="Cent Item", quantity=Decimal("1"), unit_price=Decimal("0.10"), total=Decimal("0.10"))
        ]
    )
    assert len(DocumentValidator.validate_math(data)) == 0

    data_large = InvoiceExtractionSchema(
        invoice_number="INV-LARGE-3",
        invoice_date="2024-05-01",
        subtotal=Decimal("9999999980.00"),
        tax=Decimal("19.99"),
        total_amount=Decimal("9999999999.99"),
        line_items=[
            LineItemSchema(description="Enterprise Contract", quantity=Decimal("1"), unit_price=Decimal("9999999980.00"), total=Decimal("9999999980.00"))
        ]
    )
    assert len(DocumentValidator.validate_math(data_large)) == 0


def test_invoice_date_type_model_compatibility():
    today = date(2024, 6, 15)
    invoice = ExtractedInvoice(
        document_id=9999,
        invoice_number="INV-TEST-DATE",
        invoice_date=today,
        subtotal=Decimal("50.00"),
        tax=Decimal("5.00"),
        total_amount=Decimal("55.00")
    )
    assert invoice.invoice_date == today
    assert isinstance(invoice.invoice_date, date)
    assert invoice.total_amount == Decimal("55.00")


def test_xlrd_dependency_available():
    import xlrd
    assert hasattr(xlrd, "__version__")


@patch("services.ai_extractor.OpenAI")
def test_ai_extractor_parses_numbers_directly_to_decimal(mock_openai):
    mock_instance = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = json.dumps({
        "invoice_number": "INV-DEC-AI-1",
        "invoice_date": "2024-05-20",
        "supplier_name": "Precision Corp",
        "customer_name": "Client Co",
        "subtotal": 19.99,
        "tax": 0.10,
        "total_amount": 20.09,
        "currency": "USD",
        "line_items": [
            {"description": "SaaS Fee", "quantity": 1, "unit_price": 19.99, "total": 19.99}
        ]
    })
    mock_instance.chat.completions.create.return_value.choices = [mock_choice]
    mock_openai.return_value = mock_instance

    with patch("services.ai_extractor.settings.GROQ_API_KEY", "test_key"):
        svc = AIExtractorService()
        extracted = svc.extract_from_chunk("Invoice text")

    assert isinstance(extracted.subtotal, Decimal)
    assert extracted.subtotal == Decimal("19.99")
    assert extracted.tax == Decimal("0.10")
    assert extracted.total_amount == Decimal("20.09")
    assert extracted.line_items[0].unit_price == Decimal("19.99")


def test_jsonb_line_items_serialization_preserves_exact_precision():
    items = [
        LineItemSchema(description="Item A", quantity=Decimal("3"), unit_price=Decimal("0.10"), total=Decimal("0.30")),
        LineItemSchema(description="Item B", quantity=Decimal("1"), unit_price=Decimal("19.99"), total=Decimal("19.99")),
        LineItemSchema(description="Large Item", quantity=Decimal("1"), unit_price=Decimal("9999999999.99"), total=Decimal("9999999999.99")),
    ]
    serialized = normalize_line_items_for_jsonb(items)
    roundtrip = json.loads(json.dumps(serialized))

    assert roundtrip[0]["unit_price"] == "0.10"
    assert roundtrip[0]["total"] == "0.30"
    assert roundtrip[1]["unit_price"] == "19.99"
    assert roundtrip[2]["total"] == "9999999999.99"


@pytest.mark.asyncio
async def test_manual_correction_api_preserves_decimal_and_jsonb_precision():
    sync_engine = create_engine(settings.SYNC_DATABASE_URL)
    doc_id = None

    with sync_engine.connect() as conn:
        doc_id = conn.execute(
            text("""
                INSERT INTO documents (owner_id, filename, file_path, file_type, file_size_bytes, status, created_at, updated_at)
                VALUES ('default', 'precision_test.pdf', :fp, '.pdf', 100, 'requires_manual_review', NOW(), NOW())
                RETURNING id
            """),
            {"fp": f"/tmp/prec_{uuid.uuid4().hex}.pdf"},
        ).scalar()
        conn.execute(
            text("""
                INSERT INTO extracted_invoices
                    (document_id, invoice_number, invoice_date, supplier_name, subtotal, tax, total_amount,
                     currency, line_items, is_manually_corrected)
                VALUES
                    (:doc_id, 'INV-PREC-API', '2024-05-01', 'Precision Supplier', 10.00, 1.00, 11.00,
                     'USD', '[]'::jsonb, FALSE)
            """),
            {"doc_id": doc_id},
        )
        conn.commit()

    test_async_engine = create_async_engine(settings.DATABASE_URL)
    TestSession = async_sessionmaker(bind=test_async_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            payload = {
                "invoice_number": "INV-PREC-API",
                "invoice_date": "2024-05-01",
                "supplier_name": "Precision Supplier",
                "subtotal": "9999999979.90",
                "tax": "20.09",
                "total_amount": "9999999999.99",
                "currency": "USD",
                "line_items": [
                    {"description": "Main Item", "quantity": "1", "unit_price": "9999999959.91", "total": "9999999959.91"},
                    {"description": "Add-on", "quantity": "1", "unit_price": "19.99", "total": "19.99"},
                ],
            }
            resp = await client.put(f"/api/documents/{doc_id}/correct", json=payload, headers=DEV_HEADERS)
            assert resp.status_code == 200
            data = resp.json()
            assert data["status"] == "validated"

            inv = data["extracted_invoice"]
            assert inv["subtotal"] == "9999999979.90"
            assert inv["tax"] == "20.09"
            assert inv["total_amount"] == "9999999999.99"
            assert inv["line_items"][0]["total"] == "9999999959.91"
            assert inv["line_items"][1]["unit_price"] == "19.99"
    finally:
        app.dependency_overrides.clear()
        await test_async_engine.dispose()
        if doc_id is not None:
            with sync_engine.connect() as conn:
                conn.execute(text("DELETE FROM documents WHERE id = :id"), {"id": doc_id})
                conn.commit()
        sync_engine.dispose()
