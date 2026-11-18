"""
Targeted regression and security tests for Phase 5.2 Part 1:
- GHR-01: Worker lease renewal, long-running >15m protection, crash recovery, concurrent worker safety
- GHR-02: /api/documents/reconcile protection (401 unauth, 403 normal user, 200 admin & internal token)
- GHR-03: Cross-tenant reference document & history isolation
"""

import os
import json
import uuid
import time
import tempfile
from datetime import datetime, timedelta
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from core.config import settings
from core.database import get_db
from main import app
from models.schemas import InvoiceExtractionSchema, LineItemSchema
from services.outbox_service import OutboxService
from tasks.processing_tasks import process_document_task, renew_processing_lease

USER_A_KEY = "ghr-user-a-key"
USER_B_KEY = "ghr-user-b-key"
ADMIN_KEY = "ghr-admin-key"
INTERNAL_TOKEN = "ghr-internal-svc-secret-token"

TEST_KEYS_JSON = json.dumps({
    USER_A_KEY: {"owner_id": "tenant_a", "role": "user"},
    USER_B_KEY: {"owner_id": "tenant_b", "role": "user"},
    ADMIN_KEY: {"owner_id": "platform_admin", "role": "admin"},
})


def test_ghr01_long_running_job_heartbeat_prevents_requeue_beyond_15_minutes():
    """
    GHR-01: Simulates a job running beyond 15 minutes (updated_at = 20m ago) whose active worker
    renews its lease via heartbeat. Reconciliation MUST NOT re-queue or steal the active job.
    """
    engine = create_engine(settings.SYNC_DATABASE_URL)
    Session = sessionmaker(bind=engine)
    doc_id = None

    try:
        with engine.connect() as conn:
            doc_id = conn.execute(
                text("""
                    INSERT INTO documents
                        (owner_id, filename, file_path, file_type, file_size_bytes, status,
                         worker_id, last_heartbeat_at, processing_lease_until, created_at, updated_at)
                    VALUES
                        ('tenant_a', 'long_ocr.pdf', :fp, '.pdf', 9000, 'processing',
                         'worker-long-1', NOW() - INTERVAL '20 minutes', NOW() + INTERVAL '1 minute',
                         NOW() - INTERVAL '20 minutes', NOW() - INTERVAL '20 minutes')
                    RETURNING id
                """),
                {"fp": f"/tmp/ghr01_long_{uuid.uuid4().hex}.pdf"},
            ).scalar()
            conn.commit()

        # Worker renews its lease
        renewed = renew_processing_lease(doc_id, "worker-long-1", lease_seconds=300)
        assert renewed is True

        # Wrong worker cannot renew lease
        assert renew_processing_lease(doc_id, "rogue-worker-2", lease_seconds=300) is False

        # Reconciliation must NOT re-queue active job even though started > 15m ago
        session = Session()
        try:
            with patch("tasks.processing_tasks.process_document_task.delay") as mock_delay:
                stats = OutboxService.reconcile_pending_and_stuck_sync(session)
                # Ensure our doc_id stays 'processing'
                row = session.execute(
                    text("SELECT status, worker_id FROM documents WHERE id = :id"),
                    {"id": doc_id},
                ).mappings().first()
                assert row["status"] == "processing"
                assert row["worker_id"] == "worker-long-1"
                # Confirm no outbox entry was created for this active job
                ob_cnt = session.execute(
                    text("SELECT COUNT(*) FROM task_outbox WHERE document_id = :id"),
                    {"id": doc_id},
                ).scalar()
                assert ob_cnt == 0
        finally:
            session.close()
    finally:
        if doc_id is not None:
            with engine.connect() as conn:
                conn.execute(text("DELETE FROM documents WHERE id = :id"), {"id": doc_id})
                conn.commit()
        engine.dispose()


def test_ghr01_expired_lease_after_worker_crash_is_recovered():
    """
    GHR-01: When a worker crashes and stops renewing, processing_lease_until expires in the past.
    Reconciliation recovers the abandoned job back to 'queued' and dispatches via outbox.
    """
    engine = create_engine(settings.SYNC_DATABASE_URL)
    Session = sessionmaker(bind=engine)
    doc_id = None

    try:
        with engine.connect() as conn:
            doc_id = conn.execute(
                text("""
                    INSERT INTO documents
                        (owner_id, filename, file_path, file_type, file_size_bytes, status,
                         worker_id, last_heartbeat_at, processing_lease_until, created_at, updated_at)
                    VALUES
                        ('tenant_a', 'crashed.pdf', :fp, '.pdf', 500, 'processing',
                         'dead-worker-9', NOW() - INTERVAL '10 minutes', NOW() - INTERVAL '2 minutes',
                         NOW() - INTERVAL '10 minutes', NOW() - INTERVAL '10 minutes')
                    RETURNING id
                """),
                {"fp": f"/tmp/ghr01_crash_{uuid.uuid4().hex}.pdf"},
            ).scalar()
            conn.commit()

        session = Session()
        try:
            with patch("tasks.processing_tasks.process_document_task.delay") as mock_delay:
                stats = OutboxService.reconcile_pending_and_stuck_sync(session)
                assert stats["rescued_stuck"] >= 1
                assert any(call.args[0] == doc_id for call in mock_delay.call_args_list)

                row = session.execute(
                    text("SELECT status, worker_id, processing_lease_until FROM documents WHERE id = :id"),
                    {"id": doc_id},
                ).mappings().first()
                assert row["status"] == "queued"
                assert row["worker_id"] is None
                assert row["processing_lease_until"] is None
        finally:
            session.close()
    finally:
        if doc_id is not None:
            with engine.connect() as conn:
                conn.execute(text("DELETE FROM documents WHERE id = :id"), {"id": doc_id})
                conn.commit()
        engine.dispose()


def test_ghr01_concurrent_workers_same_document_only_one_processes():
    """
    GHR-01: Two concurrent workers attempt to process the exact same document_id simultaneously.
    Lease locking ensures only ONE parses/extracts and the second skips without corrupting state.
    """
    engine = create_engine(settings.SYNC_DATABASE_URL)
    doc_id = None
    fd, path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    with open(path, "wb") as f:
        f.write(b"%PDF-1.4\n%same-doc")

    try:
        with engine.connect() as conn:
            doc_id = conn.execute(
                text("""
                    INSERT INTO documents (owner_id, filename, file_path, file_type, file_size_bytes, status, created_at, updated_at)
                    VALUES ('tenant_a', 'same_doc.pdf', :fp, '.pdf', 64, 'queued', NOW(), NOW())
                    RETURNING id
                """),
                {"fp": path},
            ).scalar()
            conn.commit()

        extraction = InvoiceExtractionSchema(
            invoice_number=f"INV-SAME-{uuid.uuid4().hex[:6]}",
            invoice_date="2024-06-01",
            supplier_name="Single Run Supplier",
            subtotal=Decimal("100.00"),
            tax=Decimal("10.00"),
            total_amount=Decimal("110.00"),
            currency="USD",
            line_items=[
                LineItemSchema(description="Item", quantity=Decimal("1"), unit_price=Decimal("100.00"), total=Decimal("100.00"))
            ],
        )

        call_counter = {"count": 0}

        def slow_parser(_path):
            call_counter["count"] += 1
            time.sleep(0.3)
            return ("Sample invoice text", 1)

        with patch("tasks.processing_tasks.DocumentParserService.extract_full_text", side_effect=slow_parser), \
             patch("tasks.processing_tasks.AIExtractorService.extract_invoice_data", return_value=extraction):
            with ThreadPoolExecutor(max_workers=2) as pool:
                f1 = pool.submit(process_document_task, doc_id)
                time.sleep(0.05)  # Slight stagger to test active lease contention
                f2 = pool.submit(process_document_task, doc_id)
                results = sorted([f1.result(timeout=15), f2.result(timeout=15)])

        assert results == [False, True]
        assert call_counter["count"] == 1

        with engine.connect() as conn:
            row = conn.execute(
                text("SELECT status, worker_id, processing_lease_until FROM documents WHERE id = :id"),
                {"id": doc_id},
            ).mappings().first()
            assert row["status"] == "validated"
            assert row["worker_id"] is None
            assert row["processing_lease_until"] is None
    finally:
        if doc_id is not None:
            with engine.connect() as conn:
                conn.execute(text("DELETE FROM documents WHERE id = :id"), {"id": doc_id})
                conn.commit()
        engine.dispose()
        if os.path.exists(path):
            os.remove(path)


@pytest.mark.asyncio
async def test_ghr02_reconcile_authorization_and_ghr03_cross_tenant_history():
    """
    GHR-02: /api/documents/reconcile rejects unauth (401), rejects normal user (403),
            rejects bad internal token (403), allows admin (200), allows valid internal service token (200).
    GHR-03: Cross-verification & history enforce tenant isolation on both primary and reference documents.
    """
    sync_engine = create_engine(settings.SYNC_DATABASE_URL)
    test_async_engine = create_async_engine(settings.DATABASE_URL)
    TestSession = async_sessionmaker(bind=test_async_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    created_ids = []

    try:
        with sync_engine.connect() as conn:
            def _seed(owner, fname, inv_num, total):
                d_id = conn.execute(
                    text("""
                        INSERT INTO documents (owner_id, filename, file_path, file_type, file_size_bytes, status, created_at, updated_at)
                        VALUES (:ow, :fn, :fp, '.pdf', 100, 'validated', NOW(), NOW())
                        RETURNING id
                    """),
                    {"ow": owner, "fn": fname, "fp": f"/tmp/ghr_{uuid.uuid4().hex}.pdf"},
                ).scalar()
                conn.execute(
                    text("""
                        INSERT INTO extracted_invoices
                            (document_id, invoice_number, supplier_name, subtotal, tax, total_amount,
                             currency, line_items, is_manually_corrected)
                        VALUES
                            (:did, :inv, 'Vendor X', :tot, 0.00, :tot, 'USD', '[]'::jsonb, FALSE)
                    """),
                    {"did": d_id, "inv": inv_num, "tot": total},
                )
                created_ids.append(d_id)
                return d_id

            doc_a1 = _seed("tenant_a", "a1.pdf", "INV-GHR-1", Decimal("100.00"))
            doc_a2 = _seed("tenant_a", "a2_ref.pdf", "INV-GHR-1", Decimal("100.00"))
            doc_b1 = _seed("tenant_b", "b_secret_ref.pdf", "INV-GHR-1", Decimal("100.00"))

            # Simulate a legacy/admin-created history entry referencing tenant_b's doc
            conn.execute(
                text("""
                    INSERT INTO cross_verification_history
                        (document_id, reference_document_id, verification_mode, overall_status, discrepancy_count, comparison_details, created_at)
                    VALUES
                        (:d1, :d_ref, 'pdf_to_pdf', 'matched', 0, '{"reference_filename": "b_secret_ref.pdf"}'::jsonb, NOW())
                """),
                {"d1": doc_a1, "d_ref": doc_b1},
            )
            conn.commit()

        with patch.object(settings, "API_KEYS_JSON", TEST_KEYS_JSON), \
             patch.object(settings, "INTERNAL_SERVICE_TOKEN", INTERNAL_TOKEN):
            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://test") as client:
                # GHR-02 checks
                assert (await client.post("/api/documents/reconcile")).status_code == 401
                assert (await client.post("/api/documents/reconcile", headers={"X-API-Key": USER_A_KEY})).status_code == 403
                assert (await client.post("/api/documents/reconcile", headers={"X-Internal-Service-Token": "wrong-token"})).status_code == 403

                with patch("tasks.processing_tasks.process_document_task.delay"):
                    r_admin = await client.post("/api/documents/reconcile", headers={"X-API-Key": ADMIN_KEY})
                    assert r_admin.status_code == 200
                    r_internal = await client.post("/api/documents/reconcile", headers={"X-Internal-Service-Token": INTERNAL_TOKEN})
                    assert r_internal.status_code == 200

                # GHR-03 checks
                # 1. Same-tenant verification passes
                r_ok = await client.post(
                    f"/api/documents/{doc_a1}/cross-verify",
                    json={"reference_document_id": doc_a2},
                    headers={"X-API-Key": USER_A_KEY},
                )
                assert r_ok.status_code == 200
                assert r_ok.json()["overall_status"] == "matched"

                # 2. Cross-tenant reference rejected without leaking metadata
                r_cross = await client.post(
                    f"/api/documents/{doc_a1}/cross-verify",
                    json={"reference_document_id": doc_b1},
                    headers={"X-API-Key": USER_A_KEY},
                )
                assert r_cross.status_code == 403
                assert "b_secret_ref" not in r_cross.text

                # 3. Cross-tenant history access rejected
                r_hist_b = await client.get(
                    f"/api/documents/{doc_a1}/cross-verify/history",
                    headers={"X-API-Key": USER_B_KEY},
                )
                assert r_hist_b.status_code == 403

                # 4. Tenant A's history MUST NOT return the row referencing doc_b1
                r_hist_a = await client.get(
                    f"/api/documents/{doc_a1}/cross-verify/history",
                    headers={"X-API-Key": USER_A_KEY},
                )
                assert r_hist_a.status_code == 200
                ref_ids = [h["reference_document_id"] for h in r_hist_a.json()]
                assert doc_a2 in ref_ids
                assert doc_b1 not in ref_ids

                # 5. Deleted/nonexistent reference doc returns 404
                r_missing = await client.post(
                    f"/api/documents/{doc_a1}/cross-verify",
                    json={"reference_document_id": 999999},
                    headers={"X-API-Key": USER_A_KEY},
                )
                assert r_missing.status_code == 404
    finally:
        app.dependency_overrides.clear()
        await test_async_engine.dispose()
        with sync_engine.connect() as conn:
            for d_id in created_ids:
                conn.execute(text("DELETE FROM documents WHERE id = :id"), {"id": d_id})
            conn.commit()
        sync_engine.dispose()
