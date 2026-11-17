"""
Celery background worker pipeline tasks.
Implements concurrency guards, exponential backoff with jitter for transient errors,
typed AI exception handling, and idempotent DB persistence.
"""

import logging
import random
from datetime import datetime
from decimal import Decimal
import httpx
from celery.exceptions import MaxRetriesExceededError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.celery_app import celery_app
from core.config import settings
from models.document import Document, ExtractedInvoice, ValidationLog
from services.document_parser import DocumentParserService
from services.ai_extractor import (
    AIExtractorService,
    AITransientError,
    AIAuthenticationError,
    AIMalformedResponseError,
    AIExtractionError
)
from services.validator import DocumentValidator, to_decimal
from services.vector_service import VectorService

logger = logging.getLogger("processing_tasks")
logger.setLevel(logging.INFO)

sync_engine = create_engine(settings.SYNC_DATABASE_URL, pool_pre_ping=True)
SessionLocalSync = sessionmaker(bind=sync_engine, expire_on_commit=False)

TRANSIENT_EXCEPTIONS = (
    AITransientError,
    httpx.RequestError,
    httpx.HTTPStatusError,
    ConnectionError,
    TimeoutError
)


@celery_app.task(name="tasks.processing_tasks.process_document_task", bind=True, max_retries=3)
def process_document_task(self, document_id: int):
    """
    Background Celery pipeline task.
    Uses row-level locking (with_for_update) to prevent race conditions.
    Retries transient network/rate-limit exceptions using exponential backoff.
    """
    session = SessionLocalSync()
    try:
        # Concurrency & Idempotency guard: Row lock
        doc = session.query(Document).filter(Document.id == document_id).with_for_update().first()
        if not doc:
            logger.warning(f"Document #{document_id} not found in database. Aborting task.")
            return False

        if doc.status == "processing" and self.request.retries == 0:
            logger.info(f"Document #{document_id} is already being processed by another worker. Skipping.")
            return False

        doc.status = "processing"
        session.commit()

        # Step 1: Text extraction (Large PDF streaming & targeted pages)
        try:
            raw_text, _ = DocumentParserService.extract_full_text(doc.file_path)
        except Exception as parse_err:
            doc.status = "failed"
            doc.error_message = f"File parsing failed: {str(parse_err)}"
            session.commit()
            return False

        if not raw_text.strip():
            doc.status = "failed"
            doc.error_message = "No readable text extracted from document."
            session.commit()
            return False

        # Step 2: AI extraction (with typed transient/permanent exception handling)
        ai_service = AIExtractorService()
        extracted_data = ai_service.extract_invoice_data(raw_text)

        # Step 3: Deterministic Financial Validations
        val_errors = []
        val_errors.extend(DocumentValidator.validate_math(extracted_data))
        val_errors.extend(DocumentValidator.validate_required_fields(extracted_data))

        # Main Pipeline Synchronous Duplicate Check
        dup_errors = DocumentValidator.check_duplicate_invoice_sync(
            session=session,
            invoice_number=extracted_data.invoice_number,
            supplier_name=extracted_data.supplier_name,
            current_doc_id=document_id
        )
        val_errors.extend(dup_errors)

        # Step 4: Vector Embedding Generation
        summary = (
            f"Supplier: {extracted_data.supplier_name or 'N/A'}. "
            f"Invoice: {extracted_data.invoice_number or 'N/A'}. "
            f"Total: {extracted_data.total_amount or Decimal('0.00')} {extracted_data.currency or 'N/A'}. "
            f"Customer: {extracted_data.customer_name or 'N/A'}. "
            f"Text: {raw_text[:800]}"
        )
        embedding_vector = VectorService.generate_embedding(summary)

        # Date parsing
        parsed_date = None
        if extracted_data.invoice_date:
            try:
                parsed_date = datetime.strptime(extracted_data.invoice_date, "%Y-%m-%d").date()
            except ValueError:
                parsed_date = None

        # Convert line items ensuring JSON serializability
        line_items_dict = []
        for it in extracted_data.line_items:
            dump = it.model_dump()
            for k in ["quantity", "unit_price", "total"]:
                if dump.get(k) is not None:
                    dump[k] = float(dump[k])
            line_items_dict.append(dump)

        subtotal_val = to_decimal(extracted_data.subtotal)
        tax_val = to_decimal(extracted_data.tax)
        total_val = to_decimal(extracted_data.total_amount)

        # Idempotent Upsert for ExtractedInvoice
        record = session.query(ExtractedInvoice).filter(ExtractedInvoice.document_id == document_id).first()
        if not record:
            record = ExtractedInvoice(
                document_id=document_id,
                invoice_number=extracted_data.invoice_number,
                invoice_date=parsed_date,
                supplier_name=extracted_data.supplier_name,
                customer_name=extracted_data.customer_name,
                subtotal=subtotal_val,
                tax=tax_val,
                total_amount=total_val,
                currency=extracted_data.currency,
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
            record.subtotal = subtotal_val
            record.tax = tax_val
            record.total_amount = total_val
            record.currency = extracted_data.currency
            record.line_items = line_items_dict
            record.raw_text = raw_text
            record.embedding = embedding_vector

        # Idempotent replacement of Validation Logs
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

        doc.status = "requires_manual_review" if has_critical else "validated"
        doc.error_message = None
        session.commit()
        return True

    except TRANSIENT_EXCEPTIONS as trans_exc:
        session.rollback()
        retry_count = self.request.retries
        backoff = (2 ** retry_count) * 4 + random.uniform(0.5, 2.0)
        logger.warning(f"Transient error processing doc #{document_id}: {trans_exc}. Retrying in {backoff:.2f}s...")
        try:
            raise self.retry(exc=trans_exc, countdown=backoff)
        except MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for document #{document_id}.")
            doc = session.query(Document).filter(Document.id == document_id).first()
            if doc:
                doc.status = "failed"
                doc.error_message = f"Transient failure max retries exceeded: {str(trans_exc)}"
                session.commit()
            return False

    except Exception as e:
        session.rollback()
        logger.exception(f"Permanent/Unhandled error processing doc #{document_id}: {e}")
        doc = session.query(Document).filter(Document.id == document_id).first()
        if doc:
            doc.status = "failed"
            doc.error_message = str(e)
            session.commit()
        return False

    finally:
        session.close()
