"""
Unit tests for the deterministic validation and reconciliation engine.
"""

import pytest
from services.validator import DocumentValidator
from models.schemas import InvoiceExtractionSchema, LineItemSchema


def test_validation_math_success():
    """Tests arithmetic validation when sums match perfectly."""
    data = InvoiceExtractionSchema(
        invoice_number="INV-2024-001",
        invoice_date="2024-05-01",
        supplier_name="Acme Corp",
        subtotal=100.0,
        tax=10.0,
        total_amount=110.0,
        currency="USD",
        line_items=[
            LineItemSchema(description="Widget A", quantity=2, unit_price=25.0, total=50.0),
            LineItemSchema(description="Widget B", quantity=1, unit_price=50.0, total=50.0),
        ]
    )

    errors = DocumentValidator.validate_math(data)
    assert len(errors) == 0, "Expected math validation to pass with zero errors"


def test_validation_line_items_mismatch():
    """Flags discrepancy when line items sum differs from subtotal."""
    data = InvoiceExtractionSchema(
        invoice_number="INV-2024-002",
        subtotal=100.0,
        tax=10.0,
        total_amount=110.0,
        line_items=[
            LineItemSchema(description="Widget A", quantity=1, unit_price=40.0, total=40.0),
            # Sum of line items = 40.0 != subtotal 100.0
        ]
    )

    errors = DocumentValidator.validate_math(data)
    assert any(e.rule_name == "LINE_ITEMS_SUM_MISMATCH" for e in errors)


def test_validation_total_calculation_mismatch():
    """Flags discrepancy when subtotal + tax != total_amount."""
    data = InvoiceExtractionSchema(
        invoice_number="INV-2024-003",
        subtotal=100.0,
        tax=10.0,
        total_amount=150.0,  # Incorrect total (should be 110.0)
    )

    errors = DocumentValidator.validate_math(data)
    assert any(e.rule_name == "TOTAL_CALCULATION_MISMATCH" for e in errors)


def test_validation_missing_required_fields():
    """Detects missing invoice number and invalid total amount."""
    data = InvoiceExtractionSchema(
        invoice_number=None,  # Missing
        total_amount=0.0      # Zero / invalid
    )

    errors = DocumentValidator.validate_required_fields(data)
    rule_names = [e.rule_name for e in errors]
    assert "MISSING_INVOICE_NUMBER" in rule_names
    assert "INVALID_TOTAL_AMOUNT" in rule_names


def test_cross_verification_matching():
    """Verifies that cross-referencing against spreadsheet ledger records works correctly."""
    data = InvoiceExtractionSchema(
        invoice_number="INV-999",
        total_amount=250.0
    )
    reference = [
        {"invoice_number": "INV-999", "total_amount": 250.0},
        {"invoice_number": "INV-888", "total_amount": 100.0}
    ]

    errors = DocumentValidator.cross_verify_with_reference(data, reference)
    assert len(errors) == 0


def test_cross_verification_mismatch():
    """Detects amount mismatch when comparing invoice against ledger."""
    data = InvoiceExtractionSchema(
        invoice_number="INV-999",
        total_amount=250.0
    )
    reference = [
        {"invoice_number": "INV-999", "total_amount": 300.0}  # Discrepancy
    ]

    errors = DocumentValidator.cross_verify_with_reference(data, reference)
    assert any(e.rule_name == "CROSS_VERIFICATION_AMOUNT_MISMATCH" for e in errors)
