"""
Cross-document verification service supporting PDF-to-PDF and PDF-to-Spreadsheet (XLSX/XLS/CSV).
Enforces document ownership checks on both primary and reference documents before extraction checks.
"""

import os
import logging
from decimal import Decimal
from typing import List, Dict, Any, Tuple, Optional
import pandas as pd
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.document import Document, ExtractedInvoice, ValidationLog, CrossVerificationHistory
from models.schemas import InvoiceExtractionSchema, LineItemSchema
from services.validator import DocumentValidator, to_decimal, normalize_identifier

logger = logging.getLogger("cross_verification")

SPREADSHEET_EXTS = {".xlsx", ".xls", ".csv"}
DOC_IMAGE_EXTS = {".pdf", ".jpg", ".jpeg", ".png", ".tiff", ".tif"}
CROSS_VERIFICATION_RULE_PREFIXES = ("CROSS_VERIFICATION_", "RECORD_NOT_FOUND_IN_REFERENCE")


class CrossVerificationService:
    @classmethod
    def _build_schema_from_extracted(cls, inv: ExtractedInvoice) -> InvoiceExtractionSchema:
        items = []
        for it in (inv.line_items or []):
            items.append(
                LineItemSchema(
                    description=it.get("description"),
                    quantity=to_decimal(it.get("quantity")),
                    unit_price=to_decimal(it.get("unit_price")),
                    total=to_decimal(it.get("total")),
                )
            )
        return InvoiceExtractionSchema(
            invoice_number=inv.invoice_number,
            invoice_date=inv.invoice_date.strftime("%Y-%m-%d") if inv.invoice_date else None,
            supplier_name=inv.supplier_name,
            customer_name=inv.customer_name,
            subtotal=to_decimal(inv.subtotal),
            tax=to_decimal(inv.tax),
            total_amount=to_decimal(inv.total_amount),
            currency=inv.currency,
            line_items=items,
        )

    @classmethod
    def _parse_spreadsheet_reference_records(cls, file_path: str, ext: str) -> List[Dict[str, Any]]:
        dfs: List[pd.DataFrame] = []
        if ext in {".xlsx", ".xls"}:
            excel_file = pd.ExcelFile(file_path)
            for sheet in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet).fillna("")
                if not df.empty:
                    dfs.append(df)
        elif ext == ".csv":
            df = pd.read_csv(file_path).fillna("")
            if not df.empty:
                dfs.append(df)

        raw_rows: List[Dict[str, Any]] = []
        for df in dfs:
            df.columns = [str(c).strip() for c in df.columns]
            raw_rows.extend(df.to_dict(orient="records"))

        if not raw_rows:
            return []

        first_keys = {k.lower() for k in raw_rows[0].keys()}
        has_invoice_level_total = any(
            k in first_keys for k in ("total amount", "total_amount", "amount", "subtotal")
        )
        has_line_item_cols = any(
            k in first_keys for k in ("item description", "description", "unit price", "unit_price")
        )

        if has_line_item_cols and not has_invoice_level_total:
            grouped: Dict[str, Dict[str, Any]] = {}
            for row in raw_rows:
                inv_val = ""
                for key in ("Invoice Number", "invoice_number", "Invoice No", "Invoice"):
                    if row.get(key) not in [None, ""]:
                        inv_val = str(row[key]).strip()
                        break
                norm_inv = normalize_identifier(inv_val) or "__default__"

                if norm_inv not in grouped:
                    grouped[norm_inv] = {
                        "invoice_number": inv_val,
                        "supplier_name": row.get("Supplier") or row.get("Supplier Name") or row.get("supplier_name") or row.get("Vendor"),
                        "customer_name": row.get("Customer") or row.get("Customer Name") or row.get("customer_name") or row.get("Client"),
                        "currency": row.get("Currency") or row.get("currency"),
                        "line_items": [],
                        "subtotal": Decimal("0.00"),
                    }

                item_total = to_decimal(row.get("Total") or row.get("total") or row.get("Line Total")) or Decimal("0.00")
                grouped[norm_inv]["line_items"].append({
                    "description": row.get("Item Description") or row.get("Description") or row.get("description"),
                    "quantity": row.get("Quantity") or row.get("quantity") or row.get("Qty"),
                    "unit_price": row.get("Unit Price") or row.get("unit_price"),
                    "total": f"{item_total:.2f}",
                })
                grouped[norm_inv]["subtotal"] += item_total

            aggregated_records = []
            for rec in grouped.values():
                rec["subtotal"] = f"{rec['subtotal']:.2f}"
                aggregated_records.append(rec)
            return aggregated_records

        return raw_rows

    @classmethod
    def load_reference_records(cls, ref_doc: Document) -> Tuple[List[Dict[str, Any]], str]:
        ext = (ref_doc.file_type or "").lower()
        if ext in SPREADSHEET_EXTS:
            if ref_doc.file_path and os.path.exists(ref_doc.file_path):
                try:
                    records = cls._parse_spreadsheet_reference_records(ref_doc.file_path, ext)
                    if records:
                        return records, "pdf_to_spreadsheet"
                except Exception as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Failed to parse reference spreadsheet '{ref_doc.filename}': {str(e)}"
                    )
            if ref_doc.extracted_invoice:
                inv = ref_doc.extracted_invoice
                return [{
                    "invoice_number": inv.invoice_number,
                    "supplier_name": inv.supplier_name,
                    "customer_name": inv.customer_name,
                    "subtotal": inv.subtotal,
                    "tax": inv.tax,
                    "total_amount": inv.total_amount,
                    "currency": inv.currency,
                    "line_items": inv.line_items or [],
                }], "pdf_to_spreadsheet"
            raise HTTPException(status_code=400, detail="Reference spreadsheet has no readable records.")

        if ext in DOC_IMAGE_EXTS:
            if not ref_doc.extracted_invoice:
                raise HTTPException(
                    status_code=400,
                    detail=f"Reference document #{ref_doc.id} has not been extracted yet (status: {ref_doc.status})."
                )
            inv = ref_doc.extracted_invoice
            return [{
                "invoice_number": inv.invoice_number,
                "supplier_name": inv.supplier_name,
                "customer_name": inv.customer_name,
                "subtotal": inv.subtotal,
                "tax": inv.tax,
                "total_amount": inv.total_amount,
                "currency": inv.currency,
                "line_items": inv.line_items or [],
            }], "pdf_to_pdf"

        raise HTTPException(
            status_code=400,
            detail=f"Incompatible reference document format '{ext}'."
        )

    @classmethod
    async def execute_cross_verification(
        cls,
        db: AsyncSession,
        document_id: int,
        reference_document_id: int,
        owner_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        if document_id == reference_document_id:
            raise HTTPException(status_code=400, detail="Cannot cross-verify a document against itself.")

        stmt_doc = (
            select(Document)
            .options(selectinload(Document.extracted_invoice), selectinload(Document.validation_logs))
            .where(Document.id == document_id)
        )
        doc = (await db.execute(stmt_doc)).scalars().first()
        if not doc:
            raise HTTPException(status_code=404, detail=f"Document #{document_id} not found.")
        if owner_id is not None and doc.owner_id != owner_id:
            raise HTTPException(status_code=403, detail="Access denied to primary document.")

        stmt_ref = (
            select(Document)
            .options(selectinload(Document.extracted_invoice))
            .where(Document.id == reference_document_id)
        )
        ref_doc = (await db.execute(stmt_ref)).scalars().first()
        if not ref_doc:
            raise HTTPException(status_code=404, detail=f"Reference document #{reference_document_id} not found.")
        if owner_id is not None and ref_doc.owner_id != owner_id:
            raise HTTPException(status_code=403, detail="Access denied to reference document.")

        if not doc.extracted_invoice:
            raise HTTPException(
                status_code=400,
                detail=f"Document #{document_id} has incomplete extraction (status: {doc.status}). Process it first."
            )

        if ref_doc.status == "failed":
            raise HTTPException(
                status_code=400,
                detail=f"Reference document #{reference_document_id} is in 'failed' state and cannot be used for verification."
            )

        reference_records, verification_mode = cls.load_reference_records(ref_doc)
        extracted_schema = cls._build_schema_from_extracted(doc.extracted_invoice)

        val_errors, details = DocumentValidator.cross_verify_detailed(extracted_schema, reference_records)

        if not val_errors:
            overall_status = "matched"
        elif any(e.rule_name == "CROSS_VERIFICATION_SKIPPED" for e in val_errors):
            overall_status = "incomplete_data"
        elif any(e.rule_name == "RECORD_NOT_FOUND_IN_REFERENCE" for e in val_errors):
            overall_status = "missing_in_reference"
        else:
            overall_status = "mismatched"

        details["primary_filename"] = doc.filename
        details["reference_filename"] = ref_doc.filename

        existing_logs = list(doc.validation_logs or [])
        for old_log in existing_logs:
            if old_log.rule_name.startswith(CROSS_VERIFICATION_RULE_PREFIXES):
                await db.delete(old_log)

        new_val_logs = []
        has_error_or_critical = False
        for err in val_errors:
            if err.severity in ("ERROR", "CRITICAL"):
                has_error_or_critical = True
            log_entry = ValidationLog(
                document_id=document_id,
                rule_name=err.rule_name,
                error_description=err.error_description,
                severity=err.severity,
            )
            db.add(log_entry)
            new_val_logs.append(log_entry)

        if has_error_or_critical:
            doc.status = "requires_manual_review"

        history = CrossVerificationHistory(
            document_id=document_id,
            reference_document_id=reference_document_id,
            verification_mode=verification_mode,
            overall_status=overall_status,
            discrepancy_count=len(val_errors),
            comparison_details=details,
        )
        db.add(history)
        await db.commit()
        await db.refresh(history)

        return {
            "id": history.id,
            "document_id": history.document_id,
            "reference_document_id": history.reference_document_id,
            "verification_mode": history.verification_mode,
            "overall_status": history.overall_status,
            "discrepancy_count": history.discrepancy_count,
            "comparison_details": history.comparison_details,
            "validation_logs": [
                {
                    "rule_name": l.rule_name,
                    "error_description": l.error_description,
                    "severity": l.severity,
                }
                for l in new_val_logs
            ],
            "created_at": history.created_at,
        }
