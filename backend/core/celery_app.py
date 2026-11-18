"""
Celery asynchronous task broker configuration.
Uses Redis as message broker and result backend, with periodic outbox reconciliation.
"""

from celery import Celery
from core.config import settings

celery_app = Celery(
    "doc_intelligence_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["tasks.processing_tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    broker_connection_retry_on_startup=True,
    beat_schedule={
        "reconcile-pending-outbox-every-30s": {
            "task": "tasks.processing_tasks.reconcile_outbox_task",
            "schedule": 30.0,
        },
    },
)
