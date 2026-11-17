"""
Tests verifying Decimal financial precision, Date compatibility, and xlrd dependency.
"""

from decimal import Decimal
from datetime import date
import pytest
from services.validator import DocumentValidator, to_decimal
from models.schemas import InvoiceExtractionSchema, LineItemSchema
from models.document import ExtractedInvoice


def test_decimal_subtotal_tax_addition_precision():
    """Ensures exact monetary addition without floating-point precision issues."""
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

    errors = DocumentValidator.validate_math(data)
    assert len(errors) == 0


def test_floating_point_rounding_discrepancy_prevention():
    """
    Tests cases where binary float arithmetic typically fails (e.g., 0.1 + 0.2 = 0.30000000000000004).
    Decimal should treat 0.10 + 0.20 == 0.30 perfectly.
    """
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

    errors = DocumentValidator.validate_math(data)
    assert len(errors) == 0


def test_invoice_date_type_model_compatibility():
    """Validates that ExtractedInvoice model accepts python datetime.date objects."""
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
    """Verifies xlrd is installed and can be imported for .xls parsing."""
    import xlrd
    assert hasattr(xlrd, "__version__")
