"""
Deterministic validation engine.
Passes validation if mathematical sums match and core financial amounts exist.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from models.document import ExtractedInvoice
from models.schemas import InvoiceExtractionSchema


class ValidationRuleResult:
    def __init__(self, rule_name: str, passed: bool, error_description: str = "", severity: str = "WARNING"):
        self.rule_name = rule_name
        self.passed = passed
        self.error_description = error_description
        self.severity = severity


class DocumentValidator:
    TOLERANCE: float = 0.05

    @classmethod
    def validate_math(cls, data: InvoiceExtractionSchema) -> List[ValidationRuleResult]:
        results = []
        if data.line_items and len(data.line_items) > 0 and data.subtotal is not None:
            sum_lines = sum((item.total or 0.0) for item in data.line_items)
            diff = abs(sum_lines - data.subtotal)
            if diff > cls.TOLERANCE:
                results.append(
                    ValidationRuleResult(
                        rule_name="LINE_ITEMS_SUM_MISMATCH",
                        passed=False,
                        error_description=f"Line items total ({sum_lines:.2f}) != subtotal ({data.subtotal:.2f})",
                        severity="ERROR"
                    )
                )

        if data.subtotal is not None and data.total_amount is not None:
            tax = data.tax or 0.0
            expected = data.subtotal + tax
            diff = abs(expected - data.total_amount)
            if diff > cls.TOLERANCE:
                results.append(
                    ValidationRuleResult(
                        rule_name="TOTAL_CALCULATION_MISMATCH",
                        passed=False,
                        error_description=f"Subtotal ({data.subtotal:.2f}) + Tax ({tax:.2f}) != Total ({data.total_amount:.2f})",
                        severity="ERROR"
                    )
                )
        return results

    @classmethod
    def validate_required_fields(cls, data: InvoiceExtractionSchema) -> List[ValidationRuleResult]:
        results = []
        if not data.invoice_number:
            results.append(
                ValidationRuleResult(
                    rule_name="MISSING_INVOICE_NUMBER",
                    passed=False,
                    error_description="Invoice number is missing.",
                    severity="ERROR"
                )
            )

        if data.total_amount is None or data.total_amount <= 0:
            results.append(
                ValidationRuleResult(
                    rule_name="INVALID_TOTAL_AMOUNT",
                    passed=False,
                    error_description="Total amount is missing or invalid.",
                    severity="CRITICAL"
                )
            )

        if not data.invoice_date:
            results.append(
                ValidationRuleResult(
                    rule_name="MISSING_INVOICE_DATE",
                    passed=False,
                    error_description="Invoice date is not specified.",
                    severity="WARNING"
                )
            )
        return results

    @classmethod
    async def check_duplicate_invoice(
        cls, db: AsyncSession, invoice_number: Optional[str], supplier_name: Optional[str], current_doc_id: int
    ) -> List[ValidationRuleResult]:
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
                    error_description=f"Duplicate invoice '{invoice_number}' detected in document #{existing.document_id}",
                    severity="CRITICAL"
                )
            )
        return results

    @classmethod
    def cross_verify_with_reference(cls, extracted: InvoiceExtractionSchema, reference_records: List[Dict[str, Any]]):
        return []
