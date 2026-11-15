"""
Deterministic validation and reconciliation engine.
Performs mathematical integrity checks, required field assertions,
duplicate invoice detection, and cross-document reconciliation.
"""

from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from models.document import ExtractedInvoice
from models.schemas import InvoiceExtractionSchema


class ValidationRuleResult:
    """Represents the outcome of an individual validation rule."""
    def __init__(self, rule_name: str, passed: bool, error_description: str = "", severity: str = "WARNING"):
        self.rule_name = rule_name
        self.passed = passed
        self.error_description = error_description
        self.severity = severity  # WARNING, ERROR, CRITICAL


class DocumentValidator:
    """
    Validates extracted invoice data against business rules and mathematical checks.
    """
    TOLERANCE: float = 0.05  # Allow up to 0.05 discrepancy for floating point rounding

    @classmethod
    def validate_math(cls, data: InvoiceExtractionSchema) -> List[ValidationRuleResult]:
        """
        Validates line item summation and tax-inclusive subtotal arithmetic.
        """
        results = []

        # Rule 1: Sum of Line Items == Subtotal
        if data.line_items and len(data.line_items) > 0 and data.subtotal is not None:
            sum_lines = sum((item.total or 0.0) for item in data.line_items)
            diff = abs(sum_lines - data.subtotal)
            if diff > cls.TOLERANCE:
                results.append(
                    ValidationRuleResult(
                        rule_name="LINE_ITEMS_SUM_MISMATCH",
                        passed=False,
                        error_description=(
                            f"Sum of line items ({sum_lines:.2f}) does not match "
                            f"stated subtotal ({data.subtotal:.2f}). Discrepancy: {diff:.2f}"
                        ),
                        severity="ERROR"
                    )
                )

        # Rule 2: Subtotal + Tax == Total Amount
        if data.subtotal is not None and data.total_amount is not None:
            tax = data.tax or 0.0
            expected_total = data.subtotal + tax
            diff = abs(expected_total - data.total_amount)
            if diff > cls.TOLERANCE:
                results.append(
                    ValidationRuleResult(
                        rule_name="TOTAL_CALCULATION_MISMATCH",
                        passed=False,
                        error_description=(
                            f"Subtotal ({data.subtotal:.2f}) + Tax ({tax:.2f}) = {expected_total:.2f}, "
                            f"which does not match Total Amount ({data.total_amount:.2f}). Discrepancy: {diff:.2f}"
                        ),
                        severity="ERROR"
                    )
                )

        return results

    @classmethod
    def validate_required_fields(cls, data: InvoiceExtractionSchema) -> List[ValidationRuleResult]:
        """
        Ensures foundational financial invoice fields are present and valid.
        """
        results = []

        if not data.invoice_number or not str(data.invoice_number).strip():
            results.append(
                ValidationRuleResult(
                    rule_name="MISSING_INVOICE_NUMBER",
                    passed=False,
                    error_description="Invoice number is missing or could not be determined.",
                    severity="ERROR"
                )
            )

        if not data.invoice_date:
            results.append(
                ValidationRuleResult(
                    rule_name="MISSING_INVOICE_DATE",
                    passed=False,
                    error_description="Invoice date is missing or unformatted.",
                    severity="WARNING"
                )
            )

        if data.total_amount is None or data.total_amount <= 0:
            results.append(
                ValidationRuleResult(
                    rule_name="INVALID_TOTAL_AMOUNT",
                    passed=False,
                    error_description="Total invoice amount is missing, zero, or negative.",
                    severity="CRITICAL"
                )
            )

        return results

    @classmethod
    async def check_duplicate_invoice(
        cls, db: AsyncSession, invoice_number: Optional[str], supplier_name: Optional[str], current_doc_id: int
    ) -> List[ValidationRuleResult]:
        """
        Queries the database for existing records sharing the same invoice number and supplier.
        """
        results = []
        if not invoice_number or not supplier_name:
            return results

        stmt = select(ExtractedInvoice).where(
            and_(
                ExtractedInvoice.invoice_number == invoice_number,
                ExtractedInvoice.supplier_name.ilike(supplier_name.strip()),
                ExtractedInvoice.document_id != current_doc_id
            )
        )
        existing = (await db.execute(stmt)).scalars().first()
        if existing:
            results.append(
                ValidationRuleResult(
                    rule_name="DUPLICATE_INVOICE_DETECTED",
                    passed=False,
                    error_description=(
                        f"Invoice number '{invoice_number}' from supplier '{supplier_name}' "
                        f"already exists in document #{existing.document_id}."
                    ),
                    severity="CRITICAL"
                )
            )

        return results

    @classmethod
    def cross_verify_with_reference(
        cls,
        extracted: InvoiceExtractionSchema,
        reference_records: List[Dict[str, Any]]
    ) -> List[ValidationRuleResult]:
        """
        Cross-verifies extracted data against a reference dataset (e.g. parsed Excel ledger rows).
        Matches by invoice_number or supplier, asserting amounts match.
        """
        results = []
        if not reference_records or not extracted.invoice_number:
            return results

        matched_ref = None
        for record in reference_records:
            ref_inv = str(record.get("invoice_number", "")).strip()
            if ref_inv and ref_inv.lower() == str(extracted.invoice_number).strip().lower():
                matched_ref = record
                break

        if not matched_ref:
            results.append(
                ValidationRuleResult(
                    rule_name="CROSS_VERIFICATION_NOT_FOUND",
                    passed=False,
                    error_description=(
                        f"Invoice number '{extracted.invoice_number}' was not found in the reference spreadsheet."
                    ),
                    severity="WARNING"
                )
            )
            return results

        # Compare total amounts if reference contains it
        ref_total = matched_ref.get("total_amount") or matched_ref.get("total")
        if ref_total is not None and extracted.total_amount is not None:
            try:
                ref_total_flt = float(ref_total)
                diff = abs(ref_total_flt - extracted.total_amount)
                if diff > cls.TOLERANCE:
                    results.append(
                        ValidationRuleResult(
                            rule_name="CROSS_VERIFICATION_AMOUNT_MISMATCH",
                            passed=False,
                            error_description=(
                                f"Extracted total ({extracted.total_amount}) does not match "
                                f"reference spreadsheet total ({ref_total_flt}). Discrepancy: {diff:.2f}"
                            ),
                            severity="CRITICAL"
                        )
                    )
            except (ValueError, TypeError):
                pass

        return results
