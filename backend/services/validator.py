"""
Deterministic validation engine.
Uses Decimal arithmetic for accurate zero-error financial reconciliation,
lossless JSONB line-item serialization, duplicate checks, and cross-document verification.
"""

import re
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Any, Optional, Tuple
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
    """Helper to cleanly parse Decimal from Decimal, str, int, or float without binary drift."""
    if val is None or val == "":
        return None
    if isinstance(val, Decimal):
        return val
    try:
        if isinstance(val, str):
            cleaned = re.sub(r"[^\d.-]", "", val.strip())
            if not cleaned or cleaned == "-":
                return None
            return Decimal(cleaned)
        return Decimal(str(val))
    except Exception:
        return None


def quantize_money(val: Any) -> Optional[Decimal]:
    """Quantizes a monetary value to exact 2 decimal places using ROUND_HALF_UP."""
    dec = to_decimal(val)
    if dec is None:
        return None
    return dec.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def normalize_line_items_for_jsonb(items: Optional[List[Any]]) -> List[Dict[str, Any]]:
    """
    Serializes line items for PostgreSQL JSONB without casting Decimal to float.
    Monetary fields (unit_price, total) are stored as fixed-scale decimal strings (e.g. '19.99', '0.10'),
    and quantity is stored as an exact decimal string.
    """
    if not items:
        return []

    serialized: List[Dict[str, Any]] = []
    for item in items:
        if hasattr(item, "model_dump"):
            raw = item.model_dump()
        elif isinstance(item, dict):
            raw = dict(item)
        else:
            continue

        qty_dec = to_decimal(raw.get("quantity"))
        unit_dec = quantize_money(raw.get("unit_price"))
        tot_dec = quantize_money(raw.get("total"))

        qty_str = None
        if qty_dec is not None:
            normalized_qty = qty_dec.normalize()
            # Avoid scientific notation like 1E+2 for clean whole numbers
            qty_str = format(normalized_qty, "f")

        serialized.append({
            "description": raw.get("description"),
            "quantity": qty_str,
            "unit_price": f"{unit_dec:.2f}" if unit_dec is not None else None,
            "total": f"{tot_dec:.2f}" if tot_dec is not None else None,
        })
    return serialized


def normalize_identifier(val: Optional[str]) -> str:
    """Normalizes string for comparison: strips whitespace, lowercases, removes punctuation."""
    if not val:
        return ""
    return re.sub(r"[\s\-_#.,]+", "", val.strip().lower())


def normalize_text(val: Optional[str]) -> str:
    """Normalizes text names for semantic equality while preserving word separation."""
    if not val:
        return ""
    return " ".join(val.strip().lower().split())


class DocumentValidator:
    TOLERANCE: Decimal = Decimal("0.05")

    @classmethod
    def validate_math(cls, data: InvoiceExtractionSchema) -> List[ValidationRuleResult]:
        results = []
        subtotal_dec = to_decimal(data.subtotal)
        total_dec = to_decimal(data.total_amount)
        tax_dec = to_decimal(data.tax) or Decimal("0.00")

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
    def cross_verify_detailed(
        cls, extracted: InvoiceExtractionSchema, reference_records: List[Dict[str, Any]]
    ) -> Tuple[List[ValidationRuleResult], Dict[str, Any]]:
        """
        Cross-verifies extracted invoice against ledger / reference records.
        """
        results: List[ValidationRuleResult] = []
        details: Dict[str, Any] = {
            "matched_invoice_number": extracted.invoice_number,
            "fields": {},
            "line_items_comparison": None,
        }

        if not extracted.invoice_number or not str(extracted.invoice_number).strip():
            err = ValidationRuleResult(
                rule_name="CROSS_VERIFICATION_SKIPPED",
                passed=False,
                error_description="Cannot cross-verify because invoice number is missing.",
                severity="WARNING"
            )
            results.append(err)
            details["status_reason"] = "missing_invoice_number"
            return results, details

        target_inv_norm = normalize_identifier(extracted.invoice_number)
        target_sup_norm = normalize_identifier(extracted.supplier_name)

        def _extract_inv(rec: Dict[str, Any]) -> str:
            for k in ["invoice_number", "Invoice Number", "Invoice No", "Invoice", "invoice_no"]:
                if rec.get(k) not in [None, ""]:
                    return str(rec[k])
            return ""

        def _extract_sup(rec: Dict[str, Any]) -> str:
            for k in ["supplier_name", "Supplier Name", "Supplier", "Vendor", "vendor_name"]:
                if rec.get(k) not in [None, ""]:
                    return str(rec[k])
            return ""

        matched_record = None
        inv_only_candidates = []
        for record in reference_records:
            ref_inv = _extract_inv(record)
            ref_sup = _extract_sup(record)
            if target_inv_norm == normalize_identifier(ref_inv):
                inv_only_candidates.append(record)
                ref_sup_norm = normalize_identifier(ref_sup)
                if target_sup_norm and ref_sup_norm:
                    if target_sup_norm == ref_sup_norm:
                        matched_record = record
                        break
                else:
                    matched_record = record
                    break

        if not matched_record and len(inv_only_candidates) == 1 and len(reference_records) == 1:
            matched_record = inv_only_candidates[0]

        if not matched_record:
            results.append(
                ValidationRuleResult(
                    rule_name="RECORD_NOT_FOUND_IN_REFERENCE",
                    passed=False,
                    error_description=f"Invoice '{extracted.invoice_number}' was not found in the reference document.",
                    severity="WARNING"
                )
            )
            details["status_reason"] = "record_not_found"
            return results, details

        def get_ref_str(keys: List[str]) -> Optional[str]:
            for k in keys:
                if k in matched_record and matched_record[k] not in [None, ""]:
                    val = str(matched_record[k]).strip()
                    if val.lower() != "nan":
                        return val
            return None

        def get_ref_decimal(keys: List[str]) -> Optional[Decimal]:
            for k in keys:
                if k in matched_record and matched_record[k] not in [None, ""]:
                    val = to_decimal(matched_record[k])
                    if val is not None:
                        return val
            return None

        ref_supplier = get_ref_str(["supplier_name", "Supplier Name", "Supplier", "Vendor", "vendor_name"])
        doc_supplier = extracted.supplier_name
        if ref_supplier and doc_supplier:
            sup_match = normalize_identifier(ref_supplier) == normalize_identifier(doc_supplier)
            details["fields"]["supplier_name"] = {
                "document": doc_supplier,
                "reference": ref_supplier,
                "matched": sup_match
            }
            if not sup_match:
                results.append(
                    ValidationRuleResult(
                        rule_name="CROSS_VERIFICATION_SUPPLIER_MISMATCH",
                        passed=False,
                        error_description=f"Supplier mismatch: Document has '{doc_supplier}', while reference has '{ref_supplier}'.",
                        severity="ERROR"
                    )
                )

        ref_customer = get_ref_str(["customer_name", "Customer Name", "Customer", "Client", "client_name"])
        doc_customer = extracted.customer_name
        if ref_customer and doc_customer:
            cust_match = normalize_text(ref_customer) == normalize_text(doc_customer)
            details["fields"]["customer_name"] = {
                "document": doc_customer,
                "reference": ref_customer,
                "matched": cust_match
            }
            if not cust_match:
                results.append(
                    ValidationRuleResult(
                        rule_name="CROSS_VERIFICATION_CUSTOMER_MISMATCH",
                        passed=False,
                        error_description=f"Customer mismatch: Document has '{doc_customer}', while reference has '{ref_customer}'.",
                        severity="WARNING"
                    )
                )

        ref_currency = get_ref_str(["currency", "Currency", "Curr"])
        doc_currency = extracted.currency
        if ref_currency and doc_currency:
            curr_match = ref_currency.strip().upper() == doc_currency.strip().upper()
            details["fields"]["currency"] = {
                "document": doc_currency.strip().upper(),
                "reference": ref_currency.strip().upper(),
                "matched": curr_match
            }
            if not curr_match:
                results.append(
                    ValidationRuleResult(
                        rule_name="CROSS_VERIFICATION_CURRENCY_MISMATCH",
                        passed=False,
                        error_description=f"Currency mismatch: Document has '{doc_currency}', while reference has '{ref_currency}'.",
                        severity="ERROR"
                    )
                )

        ref_total = get_ref_decimal(["total_amount", "Total Amount", "Total", "amount", "Amount"])
        doc_total = to_decimal(extracted.total_amount)
        if ref_total is not None and doc_total is not None:
            tot_match = abs(ref_total - doc_total) <= cls.TOLERANCE
            details["fields"]["total_amount"] = {
                "document": f"{doc_total:.2f}",
                "reference": f"{ref_total:.2f}",
                "matched": tot_match
            }
            if not tot_match:
                results.append(
                    ValidationRuleResult(
                        rule_name="CROSS_VERIFICATION_AMOUNT_MISMATCH",
                        passed=False,
                        error_description=f"Total amount mismatch: Document has {doc_total:.2f}, while reference has {ref_total:.2f}.",
                        severity="ERROR"
                    )
                )
        elif (ref_total is None) ^ (doc_total is None):
            details["fields"]["total_amount"] = {
                "document": f"{doc_total:.2f}" if doc_total is not None else None,
                "reference": f"{ref_total:.2f}" if ref_total is not None else None,
                "matched": False
            }
            results.append(
                ValidationRuleResult(
                    rule_name="CROSS_VERIFICATION_FIELD_MISSING",
                    passed=False,
                    error_description="Total amount is present in only one of the documents.",
                    severity="ERROR"
                )
            )

        ref_subtotal = get_ref_decimal(["subtotal", "Subtotal", "Sub Total"])
        doc_subtotal = to_decimal(extracted.subtotal)
        if ref_subtotal is not None and doc_subtotal is not None:
            sub_match = abs(ref_subtotal - doc_subtotal) <= cls.TOLERANCE
            details["fields"]["subtotal"] = {
                "document": f"{doc_subtotal:.2f}",
                "reference": f"{ref_subtotal:.2f}",
                "matched": sub_match
            }
            if not sub_match:
                results.append(
                    ValidationRuleResult(
                        rule_name="CROSS_VERIFICATION_SUBTOTAL_MISMATCH",
                        passed=False,
                        error_description=f"Subtotal mismatch: Document has {doc_subtotal:.2f}, while reference has {ref_subtotal:.2f}.",
                        severity="ERROR"
                    )
                )

        ref_tax = get_ref_decimal(["tax", "Tax", "VAT", "GST"])
        doc_tax = to_decimal(extracted.tax)
        if ref_tax is not None and doc_tax is not None:
            tax_match = abs(ref_tax - doc_tax) <= cls.TOLERANCE
            details["fields"]["tax"] = {
                "document": f"{doc_tax:.2f}",
                "reference": f"{ref_tax:.2f}",
                "matched": tax_match
            }
            if not tax_match:
                results.append(
                    ValidationRuleResult(
                        rule_name="CROSS_VERIFICATION_TAX_MISMATCH",
                        passed=False,
                        error_description=f"Tax mismatch: Document has {doc_tax:.2f}, while reference has {ref_tax:.2f}.",
                        severity="ERROR"
                    )
                )

        ref_items = matched_record.get("line_items")
        if extracted.line_items and isinstance(ref_items, list) and len(ref_items) > 0:
            doc_sum = sum((to_decimal(it.total) or Decimal("0.00")) for it in extracted.line_items)
            ref_sum = sum((to_decimal(it.get("total")) or Decimal("0.00")) for it in ref_items)
            count_match = len(extracted.line_items) == len(ref_items)
            sum_match = abs(doc_sum - ref_sum) <= cls.TOLERANCE

            details["line_items_comparison"] = {
                "document_count": len(extracted.line_items),
                "reference_count": len(ref_items),
                "document_items_sum": f"{doc_sum:.2f}",
                "reference_items_sum": f"{ref_sum:.2f}",
                "matched": count_match and sum_match,
            }
            if not (count_match and sum_match):
                results.append(
                    ValidationRuleResult(
                        rule_name="CROSS_VERIFICATION_LINE_ITEMS_MISMATCH",
                        passed=False,
                        error_description=(
                            f"Line items mismatch: Document has {len(extracted.line_items)} item(s) "
                            f"(sum {doc_sum:.2f}), while reference has {len(ref_items)} item(s) (sum {ref_sum:.2f})."
                        ),
                        severity="ERROR"
                    )
                )

        return results, details

    @classmethod
    def cross_verify_with_reference(
        cls, extracted: InvoiceExtractionSchema, reference_records: List[Dict[str, Any]]
    ) -> List[ValidationRuleResult]:
        """Backward-compatible wrapper returning validation rules only."""
        results, _ = cls.cross_verify_detailed(extracted, reference_records)
        return results
