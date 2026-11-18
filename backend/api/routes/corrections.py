"""
Manual correction endpoints enabling human-in-the-loop adjustments,
with owner authorization, rate limiting, lossless Decimal JSONB normalization,
dynamic re-validation, and vector embedding updates.
"""

from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from core.database import get_db
from core.security import AuthPrincipal, get_current_principal
from core.rate_limit import rate_limit_write
from models.document import Document, ValidationLog
from models.schemas import ManualCorrectionRequest, DocumentResponse, InvoiceExtractionSchema, LineItemSchema
from services.validator import DocumentValidator, to_decimal, quantize_money, normalize_line_items_for_jsonb
from services.vector_service import VectorService

router = APIRouter(prefix="/documents", tags=["Human Review & Corrections"])


@router.put("/{document_id}/correct", response_model=DocumentResponse, dependencies=[Depends(rate_limit_write)])
async def correct_invoice_data(
    document_id: int,
    payload: ManualCorrectionRequest,
    principal: AuthPrincipal = Depends(get_current_principal),
    db: AsyncSession = Depends(get_db),
):
    """Applies manual user adjustments to an owned extracted invoice."""
    query = (
        select(Document)
        .options(
            selectinload(Document.extracted_invoice),
            selectinload(Document.validation_logs),
        )
        .where(Document.id == document_id)
    )
    result = await db.execute(query)
    doc = result.scalars().first()

    if not doc:
        raise HTTPException(status_code=404, detail=f"Document #{document_id} not found.")
    if not principal.is_admin and doc.owner_id != principal.owner_id:
        raise HTTPException(status_code=403, detail="Access denied to requested document.")

    invoice = doc.extracted_invoice
    if not invoice:
        raise HTTPException(status_code=400, detail="Cannot apply corrections to a document without extracted data.")

    if payload.invoice_number is not None:
        invoice.invoice_number = payload.invoice_number
    if payload.invoice_date is not None:
        invoice.invoice_date = payload.invoice_date
    if payload.supplier_name is not None:
        invoice.supplier_name = payload.supplier_name
    if payload.customer_name is not None:
        invoice.customer_name = payload.customer_name
    if payload.subtotal is not None:
        invoice.subtotal = quantize_money(payload.subtotal)
    if payload.tax is not None:
        invoice.tax = quantize_money(payload.tax)
    if payload.total_amount is not None:
        invoice.total_amount = quantize_money(payload.total_amount)
    if payload.currency is not None:
        invoice.currency = payload.currency
    if payload.line_items is not None:
        invoice.line_items = normalize_line_items_for_jsonb(payload.line_items)

    invoice.is_manually_corrected = True

    items = []
    if invoice.line_items:
        for it in invoice.line_items:
            items.append(
                LineItemSchema(
                    description=it.get("description"),
                    quantity=to_decimal(it.get("quantity")),
                    unit_price=to_decimal(it.get("unit_price")),
                    total=to_decimal(it.get("total")),
                )
            )

    date_str = invoice.invoice_date.strftime("%Y-%m-%d") if invoice.invoice_date else None

    validation_payload = InvoiceExtractionSchema(
        invoice_number=invoice.invoice_number,
        invoice_date=date_str,
        supplier_name=invoice.supplier_name,
        customer_name=invoice.customer_name,
        subtotal=to_decimal(invoice.subtotal),
        tax=to_decimal(invoice.tax),
        total_amount=to_decimal(invoice.total_amount),
        currency=invoice.currency,
        line_items=items,
    )

    val_errors = []
    val_errors.extend(DocumentValidator.validate_math(validation_payload))
    val_errors.extend(DocumentValidator.validate_required_fields(validation_payload))

    dup_errors = await DocumentValidator.check_duplicate_invoice(
        db, invoice.invoice_number, invoice.supplier_name, current_doc_id=doc.id
    )
    val_errors.extend(dup_errors)

    await db.execute(delete(ValidationLog).where(ValidationLog.document_id == document_id))
    for err in val_errors:
        db.add(
            ValidationLog(
                document_id=document_id,
                rule_name=err.rule_name,
                error_description=err.error_description,
                severity=err.severity,
            )
        )

    doc.status = "requires_manual_review" if val_errors else "validated"

    summary = (
        f"Supplier: {invoice.supplier_name or 'N/A'}. "
        f"Invoice: {invoice.invoice_number or 'N/A'}. "
        f"Total: {invoice.total_amount or Decimal('0.00')} {invoice.currency or 'USD'}. "
        f"Customer: {invoice.customer_name or 'N/A'}."
    )
    invoice.embedding = VectorService.generate_embedding(summary)

    await db.commit()
    await db.refresh(doc)
    return doc
