"""
Manual correction endpoints enabling human-in-the-loop adjustments,
with dynamic re-validation and vector embedding updates using Decimal precision.
"""

from datetime import datetime, date
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from core.database import get_db
from models.document import Document, ExtractedInvoice, ValidationLog
from models.schemas import ManualCorrectionRequest, DocumentResponse, InvoiceExtractionSchema, LineItemSchema
from services.validator import DocumentValidator, to_decimal
from services.vector_service import VectorService

router = APIRouter(prefix="/documents", tags=["Human Review & Corrections"])


@router.put("/{document_id}/correct", response_model=DocumentResponse)
async def correct_invoice_data(
    document_id: int,
    payload: ManualCorrectionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Applies manual user adjustments to an extracted invoice.
    Re-runs deterministic validation rules and refreshes pgvector embeddings.
    """
    query = (
        select(Document)
        .options(
            selectinload(Document.extracted_invoice),
            selectinload(Document.validation_logs)
        )
        .where(Document.id == document_id)
    )
    result = await db.execute(query)
    doc = result.scalars().first()

    if not doc:
        raise HTTPException(status_code=404, detail=f"Document #{document_id} not found.")

    invoice = doc.extracted_invoice
    if not invoice:
        raise HTTPException(status_code=400, detail="Cannot apply corrections to a document without extracted data.")

    # Update invoice fields from request payload
    if payload.invoice_number is not None:
        invoice.invoice_number = payload.invoice_number
    if payload.invoice_date is not None:
        invoice.invoice_date = payload.invoice_date
    if payload.supplier_name is not None:
        invoice.supplier_name = payload.supplier_name
    if payload.customer_name is not None:
        invoice.customer_name = payload.customer_name
    if payload.subtotal is not None:
        invoice.subtotal = to_decimal(payload.subtotal)
    if payload.tax is not None:
        invoice.tax = to_decimal(payload.tax)
    if payload.total_amount is not None:
        invoice.total_amount = to_decimal(payload.total_amount)
    if payload.currency is not None:
        invoice.currency = payload.currency
    if payload.line_items is not None:
        invoice.line_items = payload.line_items

    invoice.is_manually_corrected = True

    # Build Pydantic model to re-run validation checks
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
        line_items=items
    )

    # Execute math and field assertions
    val_errors = []
    val_errors.extend(DocumentValidator.validate_math(validation_payload))
    val_errors.extend(DocumentValidator.validate_required_fields(validation_payload))

    # Duplicate check
    dup_errors = await DocumentValidator.check_duplicate_invoice(
        db, invoice.invoice_number, invoice.supplier_name, current_doc_id=doc.id
    )
    val_errors.extend(dup_errors)

    # Purge old validation logs and write new logs
    await db.execute(delete(ValidationLog).where(ValidationLog.document_id == document_id))
    for err in val_errors:
        new_log = ValidationLog(
            document_id=document_id,
            rule_name=err.rule_name,
            error_description=err.error_description,
            severity=err.severity
        )
        db.add(new_log)

    # Update document status based on re-validation
    if val_errors:
        doc.status = "requires_manual_review"
    else:
        doc.status = "validated"

    # Refresh pgvector embedding to reflect corrected fields
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
