
PHASE 5.2 — CRITICAL BUG FIXES & RELIABILITY IMPROVEMENTS COMPLETION REPORT

Date: 2026-11-18 Target Revision: Alembic 0009_lease_epoch_fencing (head)
Backend Test Suite: 83 passed, 1 warning in 16.32s 1,000-Page Capacity
Benchmark: 1,000 pages parsed in 0.42 seconds (2,360 pages/sec) with bounded
Peak RSS of 121.7 MB (net growth 0.0 MB) Live Evaluation Benchmark: 10 labeled
documents, 88.75% scalar accuracy, 98.25% 4-field strict line-item F1, 0.00%
hallucination rate Frontend Production Build: next build succeeded (5/5
routes, 0 TypeScript/lint errors)

1. Executive Summary

Phase 5.2 addressed all eight independent GitHub review findings (GHR-01 through
GHR-08) across worker reliability, authorization, tenant isolation, currency
precision, migration safety, honest multi-format benchmarking, distributed rate
limiting, and Docker secret parameterization. All code was verified against the
running PostgreSQL 16 + pgvector, Redis, FastAPI, Celery, and Next.js 14 stack.

2. GHR-01 through GHR-08 Status Summary

| Issue ID   | Severity | Status               | Summary                                                                                                                                                                                               |
| ---------- | -------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GHR-01** | Critical | **FIXED AND TESTED** | Monotonic `lease_epoch` fencing token, strict Compare-and-Set (CAS) worker fencing, heartbeat renewal thread, and active-lease guard preventing retries/concurrent workers from stealing live leases. |
| **GHR-02** | Critical | **FIXED AND TESTED** | Global `/api/documents/reconcile` restricted to `role="admin"` or valid `X-Internal-Service-Token`.                                                                                                   |
| **GHR-03** | Critical | **FIXED AND TESTED** | Cross-verification & history endpoints enforce `owner_id` on both primary and reference documents without metadata leakage.                                                                           |
| **GHR-04** | High     | **FIXED AND TESTED** | Unknown (`null`) currency is preserved end-to-end across ORM, Pydantic, corrections API, and Next.js forms/views without USD defaulting.                                                              |
| **GHR-05** | High     | **FIXED AND TESTED** | `main.py` lifespan verifies Alembic `head` and fails fast on missing/outdated migrations; `validate_production_security()` rejects placeholder secrets.                                               |
| **GHR-06** | High     | **FIXED AND TESTED** | Reproducible 10-document multi-format dataset & 12-metric evaluation pipeline executed against real OCR/PyMuPDF/Pandas/Groq with honest `not_evaluable` math classification.                          |
| **GHR-07** | Medium   | **FIXED AND TESTED** | Process-independent SHA-256 rate-limit keys and atomic Redis Lua sliding window implemented and verified across subprocesses.                                                                         |
| **GHR-08** | Medium   | **FIXED AND TESTED** | Hardcoded credentials removed from `docker-compose.yml` via `${POSTGRES_*}` environment variables, and `docker-compose.prod.yml` added.                                                               |

3. Root Cause of Each Issue

1.  GHR-01: Document lacked worker_id, processing_lease_until,
    last_heartbeat_at, and lease_epoch. OutboxService treated any processing row
    with updated_at <= now - 15m as stale, risking duplicate execution of slow
    OCR/AI jobs, while stale workers could overwrite state if worker_id was
    cleared to null.
2.  GHR-02: POST /api/documents/reconcile only checked get_current_principal,
    permitting ordinary role="user" accounts to trigger global system
    reconciliation.
3.  GHR-03: GET /api/documents/{id}/cross-verify/history did not verify current
    ownership of reference_document_id, and cross-verification error handling
    needed non-leaking responses.
4.  GHR-04: ExtractedInvoice.currency defaulted to "USD", and frontend pages
    used currency || 'USD', causing edits to overwrite null currency with "USD".
5.  GHR-05: main.py wrapped await init_db() in a broad try...except that logged
    and swallowed failures, allowing startup with missing or behind-head
    migrations.
6.  GHR-06: evaluation/evaluate.py previously evaluated only 3 text-only
    snippets without running OCR/PDF/Excel parsing, without measuring line items
    or hallucination rate, and without mounting ./evaluation in Docker.
7.  GHR-07: core/rate_limit.py used Python's randomized hash(api_key)
    (inconsistent across workers) and non-atomic Redis pipeline commands that
    still wrote rejected hits.
8.  GHR-08: docker-compose.yml hardcoded postgres:postgres connection strings in
    backend and celery_worker service environments.

4. Implementation Details

  - GHR-01 (models/document.py, 0007, 0009, processing_tasks.py,
    outbox_service.py): Added worker_id, processing_lease_until,
    last_heartbeat_at, and lease_epoch to documents. Workers claim an atomic
    lease, spawn a daemon _LeaseHeartbeat thread renewing every 60s, and apply a
    strict Compare-and-Set (CAS) guard at Step 5 (session.expire_all() + check
    doc.status == 'processing' and doc.worker_id == worker_id and
    doc.lease_epoch == claimed_epoch). /reprocess rejects active leases with 409
    Conflict.
  - GHR-02 (core/security.py, routes/documents.py): Added
    require_admin_or_internal checking constant-time X-Internal-Service-Token or
    principal.is_admin, applied to POST /api/documents/reconcile.
  - GHR-03 (routes/documents.py, services/cross_verification_service.py): Added
    aliased(Document) join on reference_document_id in
    get_cross_verification_history filtering ref_doc.owner_id ==
    principal.owner_id, returning 403 without leaking reference metadata.
  - GHR-04 (models/document.py, 0008, models/schemas.py, routes/corrections.py,
    frontend/app/**): Removed ORM default="USD" (default=None), dropped column
    default via 0008, added _normalize_currency validator and model_fields_set
    handling, and updated frontend pages to preserve blank/null currency.
  - GHR-05 (core/config.py, core/database.py, main.py, MIGRATIONS.md): Added
    verify_migration_status_sync() and MigrationSafetyError,
    validate_production_security() rejecting weak secrets/placeholders, and
    removed silent exception swallowing in main.py lifespan.
  - GHR-06 (evaluation/generate_dataset.py, evaluation/evaluate.py,
    evaluation/benchmark_large_pdf.py): Built deterministic 10-document
    multi-format generator and 12-metric evaluator with strict 4-field line-item
    matching and not_evaluable arithmetic classification. Generated and
    streamed 100-, 500-, and 1,000-page PDFs with empirical RSS tracking.
  - GHR-07 (core/rate_limit.py): Implemented compute_rate_limit_subject() using
    hashlib.sha256 and atomic Redis Lua script _SLIDING_WINDOW_LUA.
  - GHR-08 (docker-compose.yml, docker-compose.prod.yml, .env.example): Replaced
    hardcoded credentials with ${POSTGRES_*} and ${DOCKER_REDIS_URL} env vars,
    created production compose override, and mounted
    ./evaluation:/app/evaluation.

5. Actual Test & Benchmark Execution Evidence

1.  Alembic Database Migrations: alembic current -> 0009_lease_epoch_fencing
    (head)
2.  Backend Automated Pytest Suite: pytest tests/ -v -> 83 passed, 1 warning
    in 16.32s (100% Passed)
3.  1,000-Page PDF Capacity Benchmark
    (evaluation/large_pdf_benchmark_report.md):
      - 100 pages: 0.04s (2,594.7 pages/sec), Peak RSS: 120.2 MB (Growth: 0.7
        MB)
      - 500 pages: 0.16s (3,179.2 pages/sec), Peak RSS: 120.8 MB (Growth: 0.0
        MB)
      - 1,000 pages: 0.42s (2,360.9 pages/sec), Peak RSS: 121.7 MB (Growth: 0.0
        MB)
4.  Live 10-Document Multi-Format Evaluation Benchmark
    (evaluation/evaluation_report.md):
      - Pipeline Execution Success: 100.00% (10/10)
      - Field Extraction Success: 90.00% (9/10; 1 unreadable noisy scan candidly
        reported)
      - Overall Scalar Field Accuracy: 88.75%
      - Line-Item 4-Field Strict F1: 98.25% (Precision: 100%, Recall: 96.55%)
      - Arithmetic Consistency (Evaluable Valid Docs): 100.00% (8/8 evaluable; 1
        unreadable scan classified as not_evaluable)
      - Discrepancy Detection: 100.00% (1/1 intentional math discrepancy caught)
      - Hallucination Rate (on Null Truth Fields): 0.00% (0/4)
      - Average Total Latency: 1.99 sec/doc (Parse/OCR: 0.61s, AI: 1.38s)
5.  Frontend Production Build: npm run build -> ✓ Compiled successfully, ✓
    Linting and checking validity of types, Generating static pages (5/5). 
