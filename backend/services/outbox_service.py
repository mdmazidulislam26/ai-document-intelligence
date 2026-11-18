"""
Transactional outbox dispatch and lease-aware reconciliation service.
Increments lease_epoch on recovery so any stale previous worker is permanently fenced out.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from models.document import Document, TaskOutbox

logger = logging.getLogger("outbox_service")


class OutboxService:
    STUCK_QUEUED_THRESHOLD_SECONDS = 60
    ORPHAN_NO_LEASE_THRESHOLD_MINUTES = 15
    DISPATCH_RETRY_BACKOFF_SECONDS = 15

    @classmethod
    async def dispatch_outbox_entries_async(cls, db: AsyncSession, outbox_ids: List[int]) -> Dict[str, int]:
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
                logger.error(f"Outbox #{entry.id} dispatch failed for doc #{entry.document_id}: {type(broker_err).__name__}")

        await db.commit()
        return {"dispatched": dispatched, "failed": failed}

    @classmethod
    async def reconcile_pending_and_stuck_async(cls, db: AsyncSession) -> Dict[str, int]:
        now = datetime.utcnow()
        rescued_stuck = 0

        queued_cutoff = now - timedelta(seconds=cls.STUCK_QUEUED_THRESHOLD_SECONDS)
        stuck_docs_stmt = select(Document).where(
            and_(
                Document.status == "queued",
                Document.updated_at <= queued_cutoff,
            )
        ).with_for_update(skip_locked=True)
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
                db.add(TaskOutbox(document_id=doc.id, status="pending", next_attempt_at=now))
                rescued_stuck += 1

        orphan_cutoff = now - timedelta(minutes=cls.ORPHAN_NO_LEASE_THRESHOLD_MINUTES)
        expired_lease_stmt = select(Document).where(
            and_(
                Document.status == "processing",
                or_(
                    Document.processing_lease_until <= now,
                    and_(
                        Document.processing_lease_until.is_(None),
                        Document.updated_at <= orphan_cutoff,
                    ),
                ),
            )
        ).with_for_update(skip_locked=True)
        expired_docs = (await db.execute(expired_lease_stmt)).scalars().all()

        for doc in expired_docs:
            doc.status = "queued"
            doc.worker_id = None
            doc.lease_epoch = (doc.lease_epoch or 0) + 1
            doc.processing_lease_until = None
            doc.last_heartbeat_at = None
            doc.updated_at = now
            db.add(
                TaskOutbox(
                    document_id=doc.id,
                    status="pending",
                    last_error="Recovered after worker lease expiration",
                    next_attempt_at=now,
                )
            )
            rescued_stuck += 1

        await db.flush()

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
        from tasks.processing_tasks import process_document_task

        now = datetime.utcnow()
        rescued_stuck = 0
        dispatched = 0
        failed = 0

        queued_cutoff = now - timedelta(seconds=cls.STUCK_QUEUED_THRESHOLD_SECONDS)
        stuck_docs = (
            session.query(Document)
            .filter(and_(Document.status == "queued", Document.updated_at <= queued_cutoff))
            .with_for_update(skip_locked=True)
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

        orphan_cutoff = now - timedelta(minutes=cls.ORPHAN_NO_LEASE_THRESHOLD_MINUTES)
        expired_docs = (
            session.query(Document)
            .filter(
                and_(
                    Document.status == "processing",
                    or_(
                        Document.processing_lease_until <= now,
                        and_(
                            Document.processing_lease_until.is_(None),
                            Document.updated_at <= orphan_cutoff,
                        ),
                    ),
                )
            )
            .with_for_update(skip_locked=True)
            .all()
        )
        for doc in expired_docs:
            doc.status = "queued"
            doc.worker_id = None
            doc.lease_epoch = (doc.lease_epoch or 0) + 1
            doc.processing_lease_until = None
            doc.last_heartbeat_at = None
            doc.updated_at = now
            session.add(
                TaskOutbox(
                    document_id=doc.id,
                    status="pending",
                    last_error="Recovered after worker lease expiration",
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
