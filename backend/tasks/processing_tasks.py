"""
Celery background worker pipeline tasks.
Implements:
- Idempotent state transitions (prevents duplicate processing on redelivery)
- PostgreSQL transaction-scoped advisory locks (pg_advisory_xact_lock) for concurrent duplicate detection
- Bounded exponential backoff with jitter for transient errors
- Immediate terminal failure on permanent errors and retry exhaustion
- Transactional outbox status synchronization and periodic reconciliation
"""

import hashlib
import logging
import random
from datetime import datetime
from decimal import Decimal
import httpx
from celery.exceptions import MaxRetriesExceededError
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from core.celery_app import celery_app
from core.config import settings
from models.document import Document, ExtractedInvoice, ValidationLog, TaskOutbox
from services.document_parser import DocumentParserService
from services.ai_extractor import (
    AIExtractorService,
    AITransientError,
)
from services.validator import DocumentValidator, quantize_money, normalize_line_items_for_jsonb
from services.vector_service import VectorService
from services.outbox_service import OutboxService

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


def _compute_business_lock_key(supplier_name: str, invoice_number: str) -> int:
    """Computes a deterministic signed 64-bit PostgreSQL advisory lock key for (supplier, invoice_number)."""
    raw = f"{supplier_name.strip().lower()}|{invoice_number.strip().lower()}".encode("utf-8")
    digest = hashlib.sha256(raw).digest()[:8]
    return int.from_bytes(digest, byteorder="big", signed=True)


def _mark_outbox_status(session, document_id: int, new_status: str, error_msg: str = None) -> None:
    entries = (
        session.query(TaskOutbox)
        .filter(
            TaskOutbox.document_id == document_id,
            TaskOutbox.status.in_(["pending", "dispatched"]),
        )
        .all()
    )
    for entry in entries:
        entry.status = new_status
        if error_msg:
            entry.last_error = error_msg


@celery_app.task(name="tasks.processing_tasks.process_document_task", bind=True, max_retries=3)
def process_document_task(self, document_id: int):
    """
    Idempotent background Celery pipeline task.
    """
    session = SessionLocalSync()
    try:
        doc = session.query(Document).filter(Document.id == document_id).with_for_update().first()
        if not doc:
            logger.warning(f"Document #{document_id} not found in database. Aborting task.")
            return False

        retries = getattr(self.request, "retries", 0) or 0

        # Idempotency guard: skip duplicate deliveries if already terminally processed or actively running
        if doc.status in ("validated", "requires_manual_review", "failed"):
            logger.info(f"Document #{document_id} already in terminal state '{doc.status}'. Skipping duplicate delivery.")
            _mark_outbox_status(session, document_id, "completed")
            session.commit()
            return True

        if doc.status == "processing" and retries == 0:
            logger.info(f"Document #{document_id} is already being processed by another worker. Skipping.")
            return False

        doc.status = "processing"
        session.commit()

        # Step 1: Parse file text (outside long DB lock)
        try:
            raw_text, _ = DocumentParserService.extract_full_text(doc.file_path)
        except Exception as parse_err:
            doc = session.query(Document).filter(Document.id == document_id).with_for_update().first()
            if doc:
                doc.status = "failed"
                doc.error_message = f"File parsing failed: {str(parse_err)}"
                _mark_outbox_status(session, document_id, "failed", doc.error_message)
                session.commit()
            return False

        if not raw_text.strip():
            doc = session.query(Document).filter(Document.id == document_id).with_for_update().first()
            if doc:
                doc.status = "failed"
                doc.error_message = "No readable text extracted from document."
                _mark_outbox_status(session, document_id, "failed", doc.error_message)
                session.commit()
            return False

        # Step 2: AI extraction (raises AITransientError on network/rate-limit)
        ai_service = AIExtractorService()
        extracted_data = ai_service.extract_invoice_data(raw_text)

        # Step 3: Deterministic Math & Required Field Validations
        val_errors = []
        val_errors.extend(DocumentValidator.validate_math(extracted_data))
        val_errors.extend(DocumentValidator.validate_required_fields(extracted_data))

        # Step 4: Embedding generation (CPU-bound, done before acquiring persistence locks)
        summary = (
            f"Supplier: {extracted_data.supplier_name or 'N/A'}. "
            f"Invoice: {extracted_data.invoice_number or 'N/A'}. "
            f"Total: {extracted_data.total_amount or Decimal('0.00')} {extracted_data.currency or 'N/A'}. "
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

        line_items_dict = normalize_line_items_for_jsonb(extracted_data.line_items)
        subtotal_val = quantize_money(extracted_data.subtotal)
        tax_val = quantize_money(extracted_data.tax)
        total_val = quantize_money(extracted_data.total_amount)

        # Step 5: Atomic Persistence Transaction with Advisory Lock for Duplicate Detection
        doc = session.query(Document).filter(Document.id == document_id).with_for_update().first()
        if not doc:
            return False

        # Serialize duplicate check + insert per (supplier_name, invoice_number) business key
        if extracted_data.invoice_number and extracted_data.supplier_name:
            lock_key = _compute_business_lock_key(extracted_data.supplier_name, extracted_data.invoice_number)
            session.execute(text("SELECT pg_advisory_xact_lock(:k)"), {"k": lock_key})

        dup_errors = DocumentValidator.check_duplicate_invoice_sync(
            session=session,
            invoice_number=extracted_data.invoice_number,
            supplier_name=extracted_data.supplier_name,
            current_doc_id=document_id
        )
        val_errors.extend(dup_errors)

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

        session.query(ValidationLog).filter(ValidationLog.document_id == document_id).delete()
        has_critical = False
        for err in val_errors:
            if err.severity in ["ERROR", "CRITICAL"]:
                has_critical = True
            session.add(
                ValidationLog(
                    document_id=document_id,
                    rule_name=err.rule_name,
                    error_description=err.error_description,
                    severity=err.severity
                )
            )

        doc.status = "requires_manual_review" if has_critical else "validated"
        doc.error_message = None
        _mark_outbox_status(session, document_id, "completed")
        session.commit()
        return True

    except TRANSIENT_EXCEPTIONS as trans_exc:
        session.rollback()
        retry_count = getattr(self.request, "retries", 0) or 0
        backoff = (2 ** retry_count) * 4 + random.uniform(0.5, 2.0)
        logger.warning(f"Transient error processing doc #{document_id}: {trans_exc}. Retrying in {backoff:.2f}s...")
        try:
            raise self.retry(exc=trans_exc, countdown=backoff)
        except MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for document #{document_id}.")
            doc = session.query(Document).filter(Document.id == document_id).with_for_update().first()
            if doc:
                doc.status = "failed"
                doc.error_message = f"Transient failure max retries exceeded: {str(trans_exc)}"
                _mark_outbox_status(session, document_id, "failed", doc.error_message)
                session.commit()
            return False

    except Exception as e:
        session.rollback()
        logger.exception(f"Permanent/Unhandled error processing doc #{document_id}: {e}")
        doc = session.query(Document).filter(Document.id == document_id).with_for_update().first()
        if doc:
            doc.status = "failed"
            doc.error_message = str(e)
            _mark_outbox_status(session, document_id, "failed", doc.error_message)
            session.commit()
        return False

    finally:
        session.close()


@celery_app.task(name="tasks.processing_tasks.reconcile_outbox_task")
def reconcile_outbox_task():
    """Periodic Celery Beat task reconciling pending outbox records and stuck documents."""
    session = SessionLocalSync()
    try:
        return OutboxService.reconcile_pending_and_stuck_sync(session)
    finally:
        session.close()
