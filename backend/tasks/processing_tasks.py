"""
Celery background worker pipeline tasks.
"""

import logging
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from core.celery_app import celery_app
from core.config import settings
from models.document import Document, ExtractedInvoice, ValidationLog
from services.document_parser import DocumentParserService
from services.ai_extractor import AIExtractorService
from services.validator import DocumentValidator
from services.vector_service import VectorService

logger = logging.getLogger("processing_tasks")
logger.setLevel(logging.INFO)

sync_engine = create_engine(settings.SYNC_DATABASE_URL, pool_pre_ping=True)
SessionLocalSync = sessionmaker(bind=sync_engine, expire_on_commit=False)


@celery_app.task(name="tasks.processing_tasks.process_document_task", bind=True, max_retries=2)
def process_document_task(self, document_id: int):
    session = SessionLocalSync()
    try:
        doc = session.query(Document).filter(Document.id == document_id).first()
        if not doc:
            return False

        doc.status = "processing"
        session.commit()

        raw_text, _ = DocumentParserService.extract_full_text(doc.file_path)
        if not raw_text.strip():
            doc.status = "failed"
            doc.error_message = "No readable text extracted."
            session.commit()
            return False

        ai_service = AIExtractorService()
        extracted_data = ai_service.extract_invoice_data(raw_text)

        # Execute validations
        val_errors = []
        val_errors.extend(DocumentValidator.validate_math(extracted_data))
        val_errors.extend(DocumentValidator.validate_required_fields(extracted_data))

        # Build embedding summary
        summary = (
            f"Supplier: {extracted_data.supplier_name or 'N/A'}. "
            f"Invoice: {extracted_data.invoice_number or 'N/A'}. "
            f"Total: {extracted_data.total_amount or 0.0} {extracted_data.currency or 'USD'}. "
            f"Customer: {extracted_data.customer_name or 'N/A'}. "
            f"Text: {raw_text[:800]}"
        )
        embedding_vector = VectorService.generate_embedding(summary)

        parsed_date = None
        if extracted_data.invoice_date:
            try:
                parsed_date = datetime.strptime(extracted_data.invoice_date, "%Y-%m-%d").date()
            except ValueError:
                parsed_date = None

        line_items_dict = [it.model_dump() for it in extracted_data.line_items]

        record = session.query(ExtractedInvoice).filter(ExtractedInvoice.document_id == document_id).first()
        if not record:
            record = ExtractedInvoice(
                document_id=document_id,
                invoice_number=extracted_data.invoice_number,
                invoice_date=parsed_date,
                supplier_name=extracted_data.supplier_name,
                customer_name=extracted_data.customer_name,
                subtotal=extracted_data.subtotal,
                tax=extracted_data.tax,
                total_amount=extracted_data.total_amount,
                currency=extracted_data.currency or "USD",
                line_items=line_items_dict,
                raw_text=raw_text,
                embedding=embedding_vector
            )
            session.add(record)
        else:
            record.invoice_number = extracted_data.invoice_number
            record.invoice_date = parsed_date
            record.supplier_name = extracted_data.supplier_name
            record.customer_name = extracted_data.customer_name
            record.subtotal = extracted_data.subtotal
            record.tax = extracted_data.tax
            record.total_amount = extracted_data.total_amount
            record.currency = extracted_data.currency or "USD"
            record.line_items = line_items_dict
            record.raw_text = raw_text
            record.embedding = embedding_vector

        session.query(ValidationLog).filter(ValidationLog.document_id == document_id).delete()
        has_critical = False
        for err in val_errors:
            if err.severity in ["ERROR", "CRITICAL"]:
                has_critical = True
            log_entry = ValidationLog(
                document_id=document_id,
                rule_name=err.rule_name,
                error_description=err.error_description,
                severity=err.severity
            )
            session.add(log_entry)

        # Only require manual review if there are real ERROR or CRITICAL mismatches
        doc.status = "requires_manual_review" if has_critical else "validated"
        session.commit()
        return True

    except Exception as e:
        session.rollback()
        logger.exception(f"Processing error doc #{document_id}: {e}")
        doc = session.query(Document).filter(Document.id == document_id).first()
        if doc:
            doc.status = "failed"
            doc.error_message = str(e)
            session.commit()
        return False
    finally:
        session.close()
