"""
Celery background worker pipeline tasks.
Implements:
- Monotonic lease_epoch and strict Compare-and-Set (CAS) worker fencing (GHR-01)
- Active lease guard preventing retries or concurrent workers from stealing live leases
- Background heartbeat thread renewing leases for long-running jobs
- Monotonic advisory locking for concurrent duplicate invoice prevention
"""

import os
import socket
import uuid
import hashlib
import logging
import random
import threading
from datetime import datetime, timedelta
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


def _generate_worker_id() -> str:
    return f"{socket.gethostname()}:{os.getpid()}:{threading.get_ident()}:{uuid.uuid4().hex[:8]}"


def renew_processing_lease(document_id: int, worker_id: str, lease_seconds: int = None, expected_epoch: int = None) -> bool:
    """
    Atomically renews processing_lease_until and last_heartbeat_at ONLY if this worker_id
    and expected_epoch still own the active 'processing' lease for document_id.
    """
    lease_secs = lease_seconds if lease_seconds is not None else settings.WORKER_LEASE_SECONDS
    now = datetime.utcnow()
    new_lease = now + timedelta(seconds=lease_secs)

    hb_session = SessionLocalSync()
    try:
        query = (
            hb_session.query(Document)
            .filter(
                Document.id == document_id,
                Document.status == "processing",
                Document.worker_id == worker_id,
            )
        )
        if expected_epoch is not None:
            query = query.filter(Document.lease_epoch == expected_epoch)

        updated = query.update(
            {
                Document.last_heartbeat_at: now,
                Document.processing_lease_until: new_lease,
                Document.updated_at: now,
            },
            synchronize_session=False,
        )
        hb_session.commit()
        return bool(updated and updated > 0)
    except Exception as hb_err:
        hb_session.rollback()
        logger.warning(f"Heartbeat renewal error for doc #{document_id}: {type(hb_err).__name__}")
        return False
    finally:
        hb_session.close()


class _LeaseHeartbeat:
    """Context manager maintaining a background lease-renewal thread during long OCR/AI jobs."""

    def __init__(self, document_id: int, worker_id: str, expected_epoch: int = None, interval_seconds: int = None, lease_seconds: int = None):
        self.document_id = document_id
        self.worker_id = worker_id
        self.expected_epoch = expected_epoch
        self.interval = interval_seconds if interval_seconds is not None else settings.WORKER_HEARTBEAT_INTERVAL_SECONDS
        self.lease_seconds = lease_seconds if lease_seconds is not None else settings.WORKER_LEASE_SECONDS
        self._stop_event = threading.Event()
        self._thread = None

    def _run(self) -> None:
        while not self._stop_event.wait(self.interval):
            still_owned = renew_processing_lease(
                self.document_id,
                self.worker_id,
                lease_seconds=self.lease_seconds,
                expected_epoch=self.expected_epoch,
            )
            if not still_owned:
                break

    def __enter__(self):
        if self.interval > 0:
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop_event.set()
        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=2.0)


def _compute_business_lock_key(supplier_name: str, invoice_number: str) -> int:
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


def _clear_lease_fields(doc: Document) -> None:
    doc.worker_id = None
    doc.processing_lease_until = None
    doc.last_heartbeat_at = None


@celery_app.task(name="tasks.processing_tasks.process_document_task", bind=True, max_retries=3)
def process_document_task(self, document_id: int):
    """
    Idempotent, lease-protected background Celery pipeline task.
    """
    session = SessionLocalSync()
    worker_id = _generate_worker_id()
    doc = None

    try:
        doc = session.query(Document).filter(Document.id == document_id).with_for_update().first()
        if not doc:
            logger.warning(f"Document #{document_id} not found in database. Aborting task.")
            return False

        now = datetime.utcnow()

        # 1. Idempotency guard on terminal states
        if doc.status in ("validated", "requires_manual_review", "failed"):
            logger.info(f"Document #{document_id} already in terminal state '{doc.status}'. Skipping delivery.")
            _mark_outbox_status(session, document_id, "completed")
            session.commit()
            return True

        # 2. Active lease guard (GHR-01): NEVER allow retries or concurrent workers to steal an active lease
        if doc.status == "processing":
            lease_until = getattr(doc, "processing_lease_until", None)
            current_worker = getattr(doc, "worker_id", None)
            if isinstance(lease_until, datetime) and lease_until > now and current_worker != worker_id:
                logger.info(
                    f"Document #{document_id} holds active lease until {lease_until.isoformat()} "
                    f"(worker={current_worker}). Skipping delivery."
                )
                return False

        # 3. Claim lease and monotonically increment lease_epoch (fencing token)
        claimed_epoch = (getattr(doc, "lease_epoch", 0) or 0) + 1
        doc.status = "processing"
        doc.worker_id = worker_id
        doc.lease_epoch = claimed_epoch
        doc.last_heartbeat_at = now
        doc.processing_lease_until = now + timedelta(seconds=settings.WORKER_LEASE_SECONDS)
        session.commit()

        # Step 1 & 2: Parse text and run AI extraction under background lease heartbeat
        with _LeaseHeartbeat(document_id=document_id, worker_id=worker_id, expected_epoch=claimed_epoch):
            try:
                raw_text, _ = DocumentParserService.extract_full_text(doc.file_path)
            except Exception as parse_err:
                doc.status = "failed"
                doc.error_message = f"File parsing failed: {str(parse_err)}"
                _clear_lease_fields(doc)
                _mark_outbox_status(session, document_id, "failed", doc.error_message)
                session.commit()
                return False

            if not raw_text.strip():
                doc.status = "failed"
                doc.error_message = "No readable text extracted from document."
                _clear_lease_fields(doc)
                _mark_outbox_status(session, document_id, "failed", doc.error_message)
                session.commit()
                return False

            ai_service = AIExtractorService()
            extracted_data = ai_service.extract_invoice_data(raw_text)

            val_errors = []
            val_errors.extend(DocumentValidator.validate_math(extracted_data))
            val_errors.extend(DocumentValidator.validate_required_fields(extracted_data))

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

        # Step 5: Final Persistence with Strict CAS Fencing Guard
        session.expire_all()
        doc = session.query(Document).filter(Document.id == document_id).with_for_update().first()
        if not doc:
            return False

        current_owner = getattr(doc, "worker_id", None)
        current_epoch = getattr(doc, "lease_epoch", 0)

        # Abort if lease expired, status changed, worker_id cleared/superseded, or epoch bumped
        if doc.status != "processing" or current_owner != worker_id or current_epoch != claimed_epoch:
            logger.warning(
                f"Document #{document_id} was fenced out. Expected worker={worker_id}, "
                f"epoch={claimed_epoch}; found status={doc.status}, worker={current_owner}, "
                f"epoch={current_epoch}. Aborting stale write."
            )
            session.rollback()
            return False

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
        _clear_lease_fields(doc)
        _mark_outbox_status(session, document_id, "completed")
        session.commit()
        return True

    except TRANSIENT_EXCEPTIONS as trans_exc:
        session.rollback()
        retry_count = getattr(self.request, "retries", 0) or 0
        backoff = (2 ** retry_count) * 4 + random.uniform(0.5, 2.0)
        logger.warning(f"Transient error processing doc #{document_id}: {type(trans_exc).__name__}. Retrying in {backoff:.2f}s...")
        try:
            raise self.retry(exc=trans_exc, countdown=backoff)
        except MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for document #{document_id}.")
            if doc:
                doc.status = "failed"
                doc.error_message = f"Transient failure max retries exceeded: {str(trans_exc)}"
                _clear_lease_fields(doc)
                _mark_outbox_status(session, document_id, "failed", doc.error_message)
                session.commit()
            return False

    except Exception as e:
        session.rollback()
        logger.exception(f"Permanent/Unhandled error processing doc #{document_id}: {type(e).__name__}")
        try:
            if doc:
                doc.status = "failed"
                doc.error_message = str(e)
                _clear_lease_fields(doc)
                _mark_outbox_status(session, document_id, "failed", doc.error_message)
                session.commit()
        except Exception:
            session.rollback()
        return False

    finally:
        session.close()


@celery_app.task(name="tasks.processing_tasks.reconcile_outbox_task")
def reconcile_outbox_task():
    """Periodic Celery Beat task reconciling pending outbox records and expired-lease documents."""
    session = SessionLocalSync()
    try:
        return OutboxService.reconcile_pending_and_stuck_sync(session)
    finally:
        session.close()
