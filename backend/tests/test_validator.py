"""
Unit tests for deterministic validation, financial decimal reconciliation,
and cross-document verification.
"""

from decimal import Decimal
import pytest
from services.validator import DocumentValidator
from models.schemas import InvoiceExtractionSchema, LineItemSchema


def test_validation_math_success():
    """Tests arithmetic validation when sums match perfectly."""
    data = InvoiceExtractionSchema(
        invoice_number="INV-2024-001",
        invoice_date="2024-05-01",
        supplier_name="Acme Corp",
        subtotal=Decimal("100.00"),
        tax=Decimal("10.00"),
        total_amount=Decimal("110.00"),
        currency="USD",
        line_items=[
            LineItemSchema(description="Widget A", quantity=Decimal("2"), unit_price=Decimal("25.00"), total=Decimal("50.00")),
            LineItemSchema(description="Widget B", quantity=Decimal("1"), unit_price=Decimal("50.00"), total=Decimal("50.00")),
        ]
    )

    errors = DocumentValidator.validate_math(data)
    assert len(errors) == 0, "Expected math validation to pass with zero errors"


def test_validation_line_items_mismatch():
    """Flags discrepancy when line items sum differs from subtotal."""
    data = InvoiceExtractionSchema(
        invoice_number="INV-2024-002",
        subtotal=Decimal("100.00"),
        tax=Decimal("10.00"),
        total_amount=Decimal("110.00"),
        line_items=[
            LineItemSchema(description="Widget A", quantity=Decimal("1"), unit_price=Decimal("40.00"), total=Decimal("40.00")),
        ]
    )

    errors = DocumentValidator.validate_math(data)
    assert any(e.rule_name == "LINE_ITEMS_SUM_MISMATCH" for e in errors)


def test_validation_total_calculation_mismatch():
    """Flags discrepancy when subtotal + tax != total_amount."""
    data = InvoiceExtractionSchema(
        invoice_number="INV-2024-003",
        subtotal=Decimal("100.00"),
        tax=Decimal("10.00"),
        total_amount=Decimal("150.00"),
    )

    errors = DocumentValidator.validate_math(data)
    assert any(e.rule_name == "TOTAL_CALCULATION_MISMATCH" for e in errors)


def test_validation_missing_required_fields():
    """Detects missing invoice number and invalid total amount."""
    data = InvoiceExtractionSchema(
        invoice_number=None,
        total_amount=Decimal("0.00")
    )

    errors = DocumentValidator.validate_required_fields(data)
    rule_names = [e.rule_name for e in errors]
    assert "MISSING_INVOICE_NUMBER" in rule_names
    assert "INVALID_TOTAL_AMOUNT" in rule_names


# -------------------------------------------------------------
# Cross-Document Verification Tests
# -------------------------------------------------------------

def test_cross_verification_matching():
    """Verifies that cross-referencing against spreadsheet ledger records works correctly."""
    data = InvoiceExtractionSchema(
        invoice_number="INV-999",
        supplier_name="Global Supplies Inc.",
        total_amount=Decimal("250.00"),
        subtotal=Decimal("230.00"),
        tax=Decimal("20.00")
    )
    reference = [
        {"invoice_number": "INV-999", "supplier_name": "Global Supplies Inc.", "total_amount": 250.00, "subtotal": 230.00, "tax": 20.00},
        {"invoice_number": "INV-888", "supplier_name": "Other Corp", "total_amount": 100.00}
    ]

    errors = DocumentValidator.cross_verify_with_reference(data, reference)
    assert len(errors) == 0


def test_cross_verification_total_mismatch():
    """Detects amount mismatch when comparing invoice against ledger."""
    data = InvoiceExtractionSchema(
        invoice_number="INV-999",
        supplier_name="Global Supplies Inc.",
        total_amount=Decimal("250.00")
    )
    reference = [
        {"invoice_number": "INV-999", "supplier_name": "Global Supplies Inc.", "total_amount": 300.00}
    ]

    errors = DocumentValidator.cross_verify_with_reference(data, reference)
    assert any(e.rule_name == "CROSS_VERIFICATION_AMOUNT_MISMATCH" for e in errors)


def test_cross_verification_subtotal_and_tax_mismatch():
    """Detects subtotal or tax discrepancy between documents."""
    data = InvoiceExtractionSchema(
        invoice_number="INV-404",
        subtotal=Decimal("150.00"),
        tax=Decimal("15.00"),
        total_amount=Decimal("165.00")
    )
    reference = [
        {"invoice_number": "INV-404", "subtotal": 140.00, "tax": 25.00, "total_amount": 165.00}
    ]

    errors = DocumentValidator.cross_verify_with_reference(data, reference)
    assert any(e.rule_name == "CROSS_VERIFICATION_SUBTOTAL_MISMATCH" for e in errors)
    assert any(e.rule_name == "CROSS_VERIFICATION_TAX_MISMATCH" for e in errors)


def test_cross_verification_missing_reference():
    """Flags when an invoice is completely missing in ledger."""
    data = InvoiceExtractionSchema(
        invoice_number="INV-MISSING-100",
        total_amount=Decimal("500.00")
    )
    reference = [
        {"invoice_number": "INV-101", "total_amount": 500.00}
    ]

    errors = DocumentValidator.cross_verify_with_reference(data, reference)
    assert any(e.rule_name == "RECORD_NOT_FOUND_IN_REFERENCE" for e in errors)


def test_cross_verification_case_and_whitespace_normalization():
    """Ensures comparison passes even with different case or dashes in invoice identifiers."""
    data = InvoiceExtractionSchema(
        invoice_number=" inv - 550 # 1 ",
        supplier_name="  NEXGEN CLOUD systems ",
        total_amount=Decimal("500.00")
    )
    reference = [
        {"invoice_number": "INV5501", "supplier_name": "Nexgen Cloud Systems", "total_amount": 500.00}
    ]

    errors = DocumentValidator.cross_verify_with_reference(data, reference)
    assert len(errors) == 0


def test_cross_verification_decimal_tolerance():
    """Allows differences within the 0.05 tolerance without flagging false errors."""
    data = InvoiceExtractionSchema(
        invoice_number="INV-TOL-1",
        total_amount=Decimal("100.03")
    )
    reference = [
        {"invoice_number": "INV-TOL-1", "total_amount": Decimal("100.00")}
    ]

    errors = DocumentValidator.cross_verify_with_reference(data, reference)
    assert len(errors) == 0
