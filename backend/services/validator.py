"""
Deterministic validation engine.
Uses Decimal arithmetic for accurate zero-error financial reconciliation,
duplicate invoice checks (sync and async), and cross-document verification.
"""

import re
from decimal import Decimal
from typing import List, Dict, Any, Optional
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from models.document import ExtractedInvoice
from models.schemas import InvoiceExtractionSchema


class ValidationRuleResult:
    def __init__(self, rule_name: str, passed: bool, error_description: str = "", severity: str = "WARNING"):
        self.rule_name = rule_name
        self.passed = passed
        self.error_description = error_description
        self.severity = severity

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_name": self.rule_name,
            "passed": self.passed,
            "error_description": self.error_description,
            "severity": self.severity
        }


def to_decimal(val: Any) -> Optional[Decimal]:
    """Helper to cleanly parse Decimal from float, string, or int."""
    if val is None or val == "":
        return None
    try:
        # Strip currency symbols and whitespace if string
        if isinstance(val, str):
            cleaned = re.sub(r"[^\d.-]", "", val.strip())
            if not cleaned or cleaned == "-":
                return None
            return Decimal(cleaned)
        return Decimal(str(val))
    except Exception:
        return None


def normalize_identifier(val: Optional[str]) -> str:
    """Normalizes string for comparison: strips whitespace, lowercases, removes non-alphanumeric."""
    if not val:
        return ""
    return re.sub(r"[\s\-_#]+", "", val.strip().lower())


class DocumentValidator:
    TOLERANCE: Decimal = Decimal("0.05")

    @classmethod
    def validate_math(cls, data: InvoiceExtractionSchema) -> List[ValidationRuleResult]:
        results = []
        subtotal_dec = to_decimal(data.subtotal)
        total_dec = to_decimal(data.total_amount)
        tax_dec = to_decimal(data.tax) or Decimal("0.00")

        # 1. Line items sum check
        if data.line_items and len(data.line_items) > 0 and subtotal_dec is not None:
            sum_lines = Decimal("0.00")
            for item in data.line_items:
                item_tot = to_decimal(item.total)
                if item_tot is not None:
                    sum_lines += item_tot

            diff = abs(sum_lines - subtotal_dec)
            if diff > cls.TOLERANCE:
                results.append(
                    ValidationRuleResult(
                        rule_name="LINE_ITEMS_SUM_MISMATCH",
                        passed=False,
                        error_description=f"Line items total ({sum_lines:.2f}) != subtotal ({subtotal_dec:.2f})",
                        severity="ERROR"
                    )
                )

        # 2. Subtotal + Tax = Total Amount check
        if subtotal_dec is not None and total_dec is not None:
            expected = subtotal_dec + tax_dec
            diff = abs(expected - total_dec)
            if diff > cls.TOLERANCE:
                results.append(
                    ValidationRuleResult(
                        rule_name="TOTAL_CALCULATION_MISMATCH",
                        passed=False,
                        error_description=f"Subtotal ({subtotal_dec:.2f}) + Tax ({tax_dec:.2f}) != Total ({total_dec:.2f})",
                        severity="ERROR"
                    )
                )
        return results

    @classmethod
    def validate_required_fields(cls, data: InvoiceExtractionSchema) -> List[ValidationRuleResult]:
        results = []
        if not data.invoice_number or not str(data.invoice_number).strip():
            results.append(
                ValidationRuleResult(
                    rule_name="MISSING_INVOICE_NUMBER",
                    passed=False,
                    error_description="Invoice number is missing.",
                    severity="ERROR"
                )
            )

        total_dec = to_decimal(data.total_amount)
        if total_dec is None or total_dec <= Decimal("0.00"):
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
        """Async duplicate check for FastAPI routes."""
        results = []
        if not invoice_number or not supplier_name:
            return results

        clean_inv = invoice_number.strip()
        clean_sup = supplier_name.strip()

        stmt = select(ExtractedInvoice).where(
            and_(
                func.lower(ExtractedInvoice.invoice_number) == clean_inv.lower(),
                func.lower(ExtractedInvoice.supplier_name) == clean_sup.lower(),
                ExtractedInvoice.document_id != current_doc_id
            )
        )
        existing = (await db.execute(stmt)).scalars().first()
        if existing:
            results.append(
                ValidationRuleResult(
                    rule_name="DUPLICATE_INVOICE_DETECTED",
                    passed=False,
                    error_description=f"Duplicate invoice '{clean_inv}' from supplier '{clean_sup}' detected in document #{existing.document_id}",
                    severity="CRITICAL"
                )
            )
        return results

    @classmethod
    def check_duplicate_invoice_sync(
        cls, session: Session, invoice_number: Optional[str], supplier_name: Optional[str], current_doc_id: int
    ) -> List[ValidationRuleResult]:
        """Synchronous duplicate check specifically for Celery workers."""
        results = []
        if not invoice_number or not supplier_name:
            return results

        clean_inv = invoice_number.strip()
        clean_sup = supplier_name.strip()

        existing = session.query(ExtractedInvoice).filter(
            and_(
                func.lower(ExtractedInvoice.invoice_number) == clean_inv.lower(),
                func.lower(ExtractedInvoice.supplier_name) == clean_sup.lower(),
                ExtractedInvoice.document_id != current_doc_id
            )
        ).first()

        if existing:
            results.append(
                ValidationRuleResult(
                    rule_name="DUPLICATE_INVOICE_DETECTED",
                    passed=False,
                    error_description=f"Duplicate invoice '{clean_inv}' from supplier '{clean_sup}' detected in document #{existing.document_id}",
                    severity="CRITICAL"
                )
            )
        return results

    @classmethod
    def cross_verify_with_reference(
        cls, extracted: InvoiceExtractionSchema, reference_records: List[Dict[str, Any]]
    ) -> List[ValidationRuleResult]:
        """
        Cross-verifies extracted invoice against ledger / reference spreadsheet records.
        Matches on normalized invoice_number and optionally supplier_name.
        Compares subtotal, tax, and total_amount using Decimal tolerance.
        """
        results = []
        if not extracted.invoice_number:
            return [
                ValidationRuleResult(
                    rule_name="CROSS_VERIFICATION_SKIPPED",
                    passed=False,
                    error_description="Cannot cross-verify because invoice number is missing.",
                    severity="WARNING"
                )
            ]

        target_inv_norm = normalize_identifier(extracted.invoice_number)
        target_sup_norm = normalize_identifier(extracted.supplier_name)

        matched_record = None
        for record in reference_records:
            ref_inv = str(record.get("invoice_number") or record.get("Invoice Number") or record.get("Invoice") or "")
            ref_sup = str(record.get("supplier_name") or record.get("Supplier") or record.get("Vendor") or "")

            ref_inv_norm = normalize_identifier(ref_inv)
            ref_sup_norm = normalize_identifier(ref_sup)

            if target_inv_norm == ref_inv_norm:
                if target_sup_norm and ref_sup_norm:
                    if target_sup_norm == ref_sup_norm:
                        matched_record = record
                        break
                else:
                    matched_record = record
                    break

        if not matched_record:
            results.append(
                ValidationRuleResult(
                    rule_name="RECORD_NOT_FOUND_IN_REFERENCE",
                    passed=False,
                    error_description=f"Invoice '{extracted.invoice_number}' was not found in the reference document.",
                    severity="WARNING"
                )
            )
            return results

        # Helper to extract monetary field from reference dictionary with varying keys
        def get_ref_field(keys: List[str]) -> Optional[Decimal]:
            for k in keys:
                if k in matched_record and matched_record[k] not in [None, ""]:
                    return to_decimal(matched_record[k])
            return None

        # Verify Total Amount
        ref_total = get_ref_field(["total_amount", "Total Amount", "Total", "amount", "Amount"])
        doc_total = to_decimal(extracted.total_amount)

        if ref_total is not None and doc_total is not None:
            if abs(ref_total - doc_total) > cls.TOLERANCE:
                results.append(
                    ValidationRuleResult(
                        rule_name="CROSS_VERIFICATION_AMOUNT_MISMATCH",
                        passed=False,
                        error_description=f"Total amount mismatch: Document has {doc_total:.2f}, while reference has {ref_total:.2f}.",
                        severity="ERROR"
                    )
                )
        elif (ref_total is None) ^ (doc_total is None):
            results.append(
                ValidationRuleResult(
                    rule_name="CROSS_VERIFICATION_FIELD_MISSING",
                    passed=False,
                    error_description="Total amount is present in only one of the documents.",
                    severity="ERROR"
                )
            )

        # Verify Subtotal if present in both
        ref_subtotal = get_ref_field(["subtotal", "Subtotal", "Sub Total"])
        doc_subtotal = to_decimal(extracted.subtotal)
        if ref_subtotal is not None and doc_subtotal is not None:
            if abs(ref_subtotal - doc_subtotal) > cls.TOLERANCE:
                results.append(
                    ValidationRuleResult(
                        rule_name="CROSS_VERIFICATION_SUBTOTAL_MISMATCH",
                        passed=False,
                        error_description=f"Subtotal mismatch: Document has {doc_subtotal:.2f}, while reference has {ref_subtotal:.2f}.",
                        severity="ERROR"
                    )
                )

        # Verify Tax if present in both
        ref_tax = get_ref_field(["tax", "Tax", "VAT", "GST"])
        doc_tax = to_decimal(extracted.tax)
        if ref_tax is not None and doc_tax is not None:
            if abs(ref_tax - doc_tax) > cls.TOLERANCE:
                results.append(
                    ValidationRuleResult(
                        rule_name="CROSS_VERIFICATION_TAX_MISMATCH",
                        passed=False,
                        error_description=f"Tax mismatch: Document has {doc_tax:.2f}, while reference has {ref_tax:.2f}.",
                        severity="ERROR"
                    )
                )

        return results
