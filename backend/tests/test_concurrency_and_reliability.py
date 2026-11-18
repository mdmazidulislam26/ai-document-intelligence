"""
Unit and PostgreSQL integration tests for Concurrency & Celery Reliability.
"""

import os
import uuid
import tempfile
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch, MagicMock
import httpx
import pytest
from celery.exceptions import MaxRetriesExceededError
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from core.config import settings
from core.database import get_db
from main import app
from models.document import Document
from models.schemas import InvoiceExtractionSchema, LineItemSchema
from tasks.processing_tasks import process_document_task

DEV_HEADERS = {"X-API-Key": "dev-local-api-key-change-me"}


def test_retry_exhaustion_marks_document_failed():
    mock_doc = MagicMock(spec=Document)
    mock_doc.id = 303
    mock_doc.file_path = "/tmp/test_retry_exhaust.pdf"
    mock_doc.status = "queued"

    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.with_for_update.return_value.first.return_value = mock_doc

    with patch("tasks.processing_tasks.SessionLocalSync", return_value=mock_session), \
         patch("tasks.processing_tasks.DocumentParserService.extract_full_text", return_value=("Sample text", 1)), \
         patch("tasks.processing_tasks.AIExtractorService.extract_invoice_data", side_effect=httpx.RequestError("Downstream timeout")), \
         patch.object(process_document_task, "retry", side_effect=MaxRetriesExceededError()):

        res = process_document_task(303)
        assert res is False
        assert mock_doc.status == "failed"
        assert "max retries exceeded" in mock_doc.error_message.lower()


def test_duplicate_delivery_is_idempotent_on_terminal_status():
    mock_doc = MagicMock(spec=Document)
    mock_doc.id = 404
    mock_doc.status = "validated"

    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.with_for_update.return_value.first.return_value = mock_doc

    with patch("tasks.processing_tasks.SessionLocalSync", return_value=mock_session), \
         patch("tasks.processing_tasks.DocumentParserService.extract_full_text") as mock_parser:
        res = process_document_task(404)
        assert res is True
        assert not mock_parser.called


def test_concurrent_duplicate_invoice_processing_no_race_condition():
    engine = create_engine(settings.SYNC_DATABASE_URL)
    doc_ids = []
    temp_files = []
    unique_inv = f"INV-RACE-{uuid.uuid4().hex[:8]}"

    try:
        with engine.connect() as conn:
            for i in range(2):
                fd, path = tempfile.mkstemp(suffix=".pdf")
                os.close(fd)
                with open(path, "wb") as f:
                    f.write(b"%PDF-1.4\n%test")
                temp_files.append(path)

                d_id = conn.execute(
                    text("""
                        INSERT INTO documents (owner_id, filename, file_path, file_type, file_size_bytes, status, created_at, updated_at)
                        VALUES ('default', :fn, :fp, '.pdf', 64, 'queued', NOW(), NOW())
                        RETURNING id
                    """),
                    {"fn": f"race_{i}.pdf", "fp": path},
                ).scalar()
                doc_ids.append(d_id)
            conn.commit()

        fixed_extraction = InvoiceExtractionSchema(
            invoice_number=unique_inv,
            invoice_date="2024-06-01",
            supplier_name="Concurrent Vendor Inc.",
            customer_name="Enterprise Client",
            subtotal=Decimal("100.00"),
            tax=Decimal("10.00"),
            total_amount=Decimal("110.00"),
            currency="USD",
            line_items=[
                LineItemSchema(description="Item 1", quantity=Decimal("1"), unit_price=Decimal("100.00"), total=Decimal("100.00"))
            ],
        )

        with patch("tasks.processing_tasks.DocumentParserService.extract_full_text", return_value=("Invoice text", 1)), \
             patch("tasks.processing_tasks.AIExtractorService.extract_invoice_data", return_value=fixed_extraction):
            with ThreadPoolExecutor(max_workers=2) as pool:
                futures = [pool.submit(process_document_task, d_id) for d_id in doc_ids]
                results = [f.result(timeout=30) for f in futures]

        assert results == [True, True]

        with engine.connect() as conn:
            statuses = []
            dup_logs = []
            for d_id in doc_ids:
                st = conn.execute(text("SELECT status FROM documents WHERE id = :id"), {"id": d_id}).scalar()
                statuses.append(st)
                logs = conn.execute(
                    text("SELECT rule_name FROM validation_logs WHERE document_id = :id"),
                    {"id": d_id},
                ).scalars().all()
                dup_logs.extend(logs)

        assert sorted(statuses) == ["requires_manual_review", "validated"]
        assert dup_logs.count("DUPLICATE_INVOICE_DETECTED") == 1
    finally:
        with engine.connect() as conn:
            for d_id in doc_ids:
                conn.execute(text("DELETE FROM documents WHERE id = :id"), {"id": d_id})
            conn.commit()
        engine.dispose()
        for path in temp_files:
            if os.path.exists(path):
                os.remove(path)


@pytest.mark.asyncio
async def test_broker_outage_outbox_recovery_and_commit_failure_safety():
    sync_engine = create_engine(settings.SYNC_DATABASE_URL)
    test_async_engine = create_async_engine(settings.DATABASE_URL)
    TestSession = async_sessionmaker(bind=test_async_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    created_doc_id = None
    created_file_path = None

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            with patch("tasks.processing_tasks.process_document_task.delay", side_effect=ConnectionError("Redis offline")):
                resp = await client.post(
                    "/api/documents/upload",
                    files=[("files", ("outbox_test.pdf", b"%PDF-1.4\n%outbox", "application/pdf"))],
                    headers=DEV_HEADERS,
                )
                assert resp.status_code == 202
                created_doc_id = resp.json()[0]["id"]

            with sync_engine.connect() as conn:
                row = conn.execute(
                    text("SELECT status, file_path FROM documents WHERE id = :id"),
                    {"id": created_doc_id},
                ).mappings().first()
                assert row["status"] == "queued"
                created_file_path = row["file_path"]

                ob = conn.execute(
                    text("SELECT status, attempts, last_error FROM task_outbox WHERE document_id = :id"),
                    {"id": created_doc_id},
                ).mappings().first()
                assert ob["status"] == "pending"
                assert ob["attempts"] >= 1
                assert "Redis offline" in ob["last_error"]

                conn.execute(
                    text("UPDATE task_outbox SET next_attempt_at = NOW() - INTERVAL '5 seconds' WHERE document_id = :id"),
                    {"id": created_doc_id},
                )
                conn.commit()

            with patch("tasks.processing_tasks.process_document_task.delay") as mock_delay:
                rec_resp = await client.post("/api/documents/reconcile", headers=DEV_HEADERS)
                assert rec_resp.status_code == 200
                rec_data = rec_resp.json()
                assert rec_data["dispatched"] >= 1
                assert mock_delay.called

            with sync_engine.connect() as conn:
                ob_after = conn.execute(
                    text("SELECT status FROM task_outbox WHERE document_id = :id"),
                    {"id": created_doc_id},
                ).scalar()
                assert ob_after == "dispatched"

            async def failing_get_db():
                async with TestSession() as session:
                    with patch.object(session, "commit", side_effect=RuntimeError("DB commit failed")):
                        yield session

            app.dependency_overrides[get_db] = failing_get_db
            with patch("tasks.processing_tasks.process_document_task.delay") as mock_delay_fail:
                resp_fail = await client.post(
                    "/api/documents/upload",
                    files=[("files", ("commit_fail.pdf", b"%PDF-1.4\n%fail", "application/pdf"))],
                    headers=DEV_HEADERS,
                )
                assert resp_fail.status_code == 500
                assert not mock_delay_fail.called
    finally:
        app.dependency_overrides.clear()
        await test_async_engine.dispose()
        if created_doc_id is not None:
            with sync_engine.connect() as conn:
                conn.execute(text("DELETE FROM documents WHERE id = :id"), {"id": created_doc_id})
                conn.commit()
        sync_engine.dispose()
        if created_file_path and os.path.exists(created_file_path):
            os.remove(created_file_path)
