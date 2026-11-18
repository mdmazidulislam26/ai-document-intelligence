"""
Transactional outbox dispatch and reconciliation service.
Ensures queued documents are never lost during Redis outages and stuck documents
are safely recovered without creating duplicate dispatches.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from models.document import Document, TaskOutbox

logger = logging.getLogger("outbox_service")


class OutboxService:
    STUCK_QUEUED_THRESHOLD_SECONDS = 60
    STALE_PROCESSING_THRESHOLD_MINUTES = 15
    DISPATCH_RETRY_BACKOFF_SECONDS = 15

    @classmethod
    async def dispatch_outbox_entries_async(cls, db: AsyncSession, outbox_ids: List[int]) -> Dict[str, int]:
        """
        Attempts to dispatch committed TaskOutbox entries via Celery after DB commit.
        Records dispatch success or schedules backoff if broker is unavailable.
        """
        from tasks.processing_tasks import process_document_task

        dispatched = 0
        failed = 0
        now = datetime.utcnow()

        for ob_id in outbox_ids:
            stmt = select(TaskOutbox).where(TaskOutbox.id == ob_id).with_for_update(skip_locked=True)
            entry = (await db.execute(stmt)).scalars().first()
            if not entry or entry.status != "pending":
                continue

            entry.attempts += 1
            try:
                process_document_task.delay(entry.document_id)
                entry.status = "dispatched"
                entry.dispatched_at = now
                entry.last_error = None
                dispatched += 1
            except Exception as broker_err:
                entry.last_error = f"Broker dispatch failed: {str(broker_err)}"
                entry.next_attempt_at = now + timedelta(seconds=cls.DISPATCH_RETRY_BACKOFF_SECONDS)
                failed += 1
                logger.error(f"Outbox #{entry.id} dispatch failed for doc #{entry.document_id}: {broker_err}")

        await db.commit()
        return {"dispatched": dispatched, "failed": failed}

    @classmethod
    async def reconcile_pending_and_stuck_async(cls, db: AsyncSession) -> Dict[str, int]:
        """
        Reconciles pending outbox records AND rescues any stuck 'queued' or stale 'processing' documents.
        """
        now = datetime.utcnow()
        rescued_stuck = 0

        # 1. Rescue documents stuck in 'queued' past threshold without any pending outbox entry
        queued_cutoff = now - timedelta(seconds=cls.STUCK_QUEUED_THRESHOLD_SECONDS)
        stuck_docs_stmt = select(Document).where(
            and_(
                Document.status == "queued",
                Document.updated_at <= queued_cutoff,
            )
        )
        stuck_docs = (await db.execute(stuck_docs_stmt)).scalars().all()

        for doc in stuck_docs:
            existing_pending = (
                await db.execute(
                    select(TaskOutbox.id).where(
                        and_(
                            TaskOutbox.document_id == doc.id,
                            TaskOutbox.status == "pending",
                        )
                    )
                )
            ).scalar()
            if not existing_pending:
                db.add(
                    TaskOutbox(
                        document_id=doc.id,
                        status="pending",
                        next_attempt_at=now,
                    )
                )
                rescued_stuck += 1

        # 2. Rescue documents stuck in 'processing' beyond stale threshold (e.g. worker crash)
        stale_cutoff = now - timedelta(minutes=cls.STALE_PROCESSING_THRESHOLD_MINUTES)
        stale_docs_stmt = select(Document).where(
            and_(
                Document.status == "processing",
                Document.updated_at <= stale_cutoff,
            )
        )
        stale_docs = (await db.execute(stale_docs_stmt)).scalars().all()
        for doc in stale_docs:
            doc.status = "queued"
            doc.updated_at = now
            db.add(
                TaskOutbox(
                    document_id=doc.id,
                    status="pending",
                    last_error="Recovered from stale processing state",
                    next_attempt_at=now,
                )
            )
            rescued_stuck += 1

        await db.flush()

        # 3. Fetch all ready pending outbox rows
        pending_stmt = select(TaskOutbox.id).where(
            and_(
                TaskOutbox.status == "pending",
                TaskOutbox.next_attempt_at <= now,
            )
        )
        pending_ids = list((await db.execute(pending_stmt)).scalars().all())
        await db.commit()

        dispatch_stats = await cls.dispatch_outbox_entries_async(db, pending_ids)
        dispatch_stats["rescued_stuck"] = rescued_stuck
        return dispatch_stats

    @classmethod
    def reconcile_pending_and_stuck_sync(cls, session: Session) -> Dict[str, int]:
        """Synchronous reconciliation used by periodic Celery Beat worker task."""
        from tasks.processing_tasks import process_document_task

        now = datetime.utcnow()
        rescued_stuck = 0
        dispatched = 0
        failed = 0

        queued_cutoff = now - timedelta(seconds=cls.STUCK_QUEUED_THRESHOLD_SECONDS)
        stuck_docs = (
            session.query(Document)
            .filter(and_(Document.status == "queued", Document.updated_at <= queued_cutoff))
            .all()
        )
        for doc in stuck_docs:
            has_pending = (
                session.query(TaskOutbox.id)
                .filter(and_(TaskOutbox.document_id == doc.id, TaskOutbox.status == "pending"))
                .first()
            )
            if not has_pending:
                session.add(TaskOutbox(document_id=doc.id, status="pending", next_attempt_at=now))
                rescued_stuck += 1

        stale_cutoff = now - timedelta(minutes=cls.STALE_PROCESSING_THRESHOLD_MINUTES)
        stale_docs = (
            session.query(Document)
            .filter(and_(Document.status == "processing", Document.updated_at <= stale_cutoff))
            .all()
        )
        for doc in stale_docs:
            doc.status = "queued"
            doc.updated_at = now
            session.add(
                TaskOutbox(
                    document_id=doc.id,
                    status="pending",
                    last_error="Recovered from stale processing state",
                    next_attempt_at=now,
                )
            )
            rescued_stuck += 1

        session.flush()

        pending_entries = (
            session.query(TaskOutbox)
            .filter(and_(TaskOutbox.status == "pending", TaskOutbox.next_attempt_at <= now))
            .with_for_update(skip_locked=True)
            .all()
        )

        for entry in pending_entries:
            entry.attempts += 1
            try:
                process_document_task.delay(entry.document_id)
                entry.status = "dispatched"
                entry.dispatched_at = now
                entry.last_error = None
                dispatched += 1
            except Exception as broker_err:
                entry.last_error = f"Broker dispatch failed: {str(broker_err)}"
                entry.next_attempt_at = now + timedelta(seconds=cls.DISPATCH_RETRY_BACKOFF_SECONDS)
                failed += 1

        session.commit()
        return {"dispatched": dispatched, "failed": failed, "rescued_stuck": rescued_stuck}
