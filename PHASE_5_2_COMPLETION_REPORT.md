# PHASE 5.2 — CRITICAL BUG FIXES & RELIABILITY IMPROVEMENTS COMPLETION REPORT

**Date:** 2026-11-18
**Target Revision:** Alembic `0008_drop_currency_default (head)`
**Backend Test Suite:** `77 passed, 1 warning in 16.19s`
**Frontend Production Build:** `next build` succeeded (`5/5` routes, 0 TypeScript/lint errors)

---

## 1. Executive Summary

Phase 5.2 addressed all eight independent GitHub review findings (**GHR-01** through **GHR-08**) across worker reliability, authorization, tenant isolation, currency precision, migration safety, honest multi-format benchmarking, distributed rate limiting, and Docker secret parameterization. The existing technology stack (FastAPI, SQLAlchemy, PostgreSQL + pgvector, Celery + Redis, Groq/Llama, FastEmbed 384-d, Next.js) was preserved without architectural rewrites.

---

## 2. GHR-01 through GHR-08 Status Summary

| Issue ID | Severity | Status | Summary |
|---|---|---|---|
| **GHR-01** | Critical | **FIXED AND TESTED** | Renewable worker lease & heartbeat thread prevent >15m active jobs from being re-queued; expired leases recover cleanly. |
| **GHR-02** | Critical | **FIXED AND TESTED** | Global `/api/documents/reconcile` restricted to `role="admin"` or valid `X-Internal-Service-Token`. |
| **GHR-03** | Critical | **FIXED AND TESTED** | Cross-verification & history endpoints enforce `owner_id` on both primary and reference documents without metadata leakage. |
| **GHR-04** | High | **FIXED AND TESTED** | Unknown (`null`) currency is preserved end-to-end across ORM, Pydantic, corrections API, and Next.js forms/views. |
| **GHR-05** | High | **FIXED AND TESTED** | `main.py` lifespan verifies Alembic `head` and fails fast on missing/outdated/failing migrations instead of swallowing errors. |
| **GHR-06** | High | **FIXED AND TESTED** | Reproducible 10-document multi-format dataset & 12-metric evaluation pipeline executed against real OCR/PyMuPDF/Pandas/Groq. |
| **GHR-07** | Medium | **FIXED AND TESTED** | Process-independent SHA-256 rate-limit keys and atomic Redis Lua sliding window implemented and verified across subprocesses. |
| **GHR-08** | Medium | **FIXED AND TESTED** | Hardcoded `postgres:postgres` credentials removed from `docker-compose.yml` in favor of `${POSTGRES_*}` and `${DOCKER_REDIS_URL}` env vars. |

---

## 3. Root Cause of Each Issue

1. **GHR-01:** `Document` lacked `worker_id`, `processing_lease_until`, and `last_heartbeat_at`. `OutboxService` treated any `processing` row with `updated_at <= now - 15m` as stale, risking duplicate execution of slow OCR/AI jobs.
2. **GHR-02:** `POST /api/documents/reconcile` only checked `get_current_principal`, permitting ordinary `role="user"` accounts to trigger global system reconciliation.
3. **GHR-03:** `GET /api/documents/{id}/cross-verify/history` did not verify current ownership of `reference_document_id`, and cross-verification error handling needed non-leaking responses.
4. **GHR-04:** `ExtractedInvoice.currency` defaulted to `"USD"`, and frontend pages used `currency || 'USD'`, causing unrelated edits to overwrite `null` currency with `"USD"`.
5. **GHR-05:** `main.py` wrapped `await init_db()` in a broad `try...except` that logged and swallowed failures, allowing startup with missing or behind-head migrations.
6. **GHR-06:** `evaluation/evaluate.py` previously evaluated only 3 text-only snippets without running OCR/PDF/Excel parsing, without measuring line items or hallucination rate, and without mounting `./evaluation` in Docker.
7. **GHR-07:** `core/rate_limit.py` used Python's randomized `hash(api_key)` (inconsistent across workers) and non-atomic Redis pipeline commands that still wrote rejected hits.
8. **GHR-08:** `docker-compose.yml` hardcoded `postgres:postgres` connection strings in `backend` and `celery_worker` service environments.

---

## 4. Implementation Details

- **GHR-01 (`backend/models/document.py`, `backend/alembic/versions/0007_worker_lease_and_currency.py`, `backend/tasks/processing_tasks.py`, `backend/services/outbox_service.py`):**
  Added `worker_id`, `processing_lease_until`, and `last_heartbeat_at` to `documents`. Workers claim an atomic lease (`WORKER_LEASE_SECONDS=300`), spawn a daemon `_LeaseHeartbeat` thread renewing every `WORKER_HEARTBEAT_INTERVAL_SECONDS=60` via `WHERE id = :id AND status = 'processing' AND worker_id = :worker_id`, verify ownership before final persistence, and clear lease fields on completion/failure. `OutboxService` only recovers `processing` documents whose `processing_lease_until <= now`.
- **GHR-02 (`backend/core/security.py`, `backend/api/routes/documents.py`):**
  Added `require_admin_or_internal` checking constant-time `X-Internal-Service-Token` or `principal.is_admin` (`role == "admin"`), applied to `POST /api/documents/reconcile`.
- **GHR-03 (`backend/api/routes/documents.py`, `backend/services/cross_verification_service.py`):**
  Added `aliased(Document)` join on `reference_document_id` in `get_cross_verification_history` filtering `ref_doc.owner_id == principal.owner_id`, and ensured cross-tenant rejections return `403` without leaking reference filenames or metadata.
- **GHR-04 (`backend/models/document.py`, `backend/alembic/versions/0008_drop_currency_default.py`, `backend/models/schemas.py`, `backend/api/routes/corrections.py`, `frontend/app/**`):**
  Removed ORM `default="USD"` (`default=None`), dropped any DB column default via `0008_drop_currency_default`, added `_normalize_currency` validator and `model_fields_set` handling in `corrections.py`, and updated `frontend/app/documents/[id]/page.tsx`, `page.tsx`, and `search/page.tsx` to preserve blank/`null` currency.
- **GHR-05 (`backend/core/config.py`, `backend/core/database.py`, `backend/main.py`, `backend/MIGRATIONS.md`):**
  Added `verify_migration_status_sync()` and `MigrationSafetyError`, `should_auto_migrate()` (disabled in `production`), and removed silent exception swallowing in `main.py` lifespan so startup aborts if migrations are unapplied, behind `head`, or unknown.
- **GHR-06 (`evaluation/generate_dataset.py`, `evaluation/evaluate.py`, `evaluation/evaluation_report.md`, `backend/services/document_parser.py`):**
  Built deterministic 10-document multi-format generator and 12-metric evaluator; improved `deskew_image()` in `document_parser.py` with Gaussian smoothing, morphological opening, and `±15°` angle cap so noisy scans aren't over-rotated.
- **GHR-07 (`backend/core/rate_limit.py`):**
  Implemented `compute_rate_limit_subject()` using `hashlib.sha256` and atomic Redis Lua script `_SLIDING_WINDOW_LUA`.
- **GHR-08 (`docker-compose.yml`, `.env.example`):**
  Replaced hardcoded credentials with `${POSTGRES_USER}`, `${POSTGRES_PASSWORD}`, `${POSTGRES_DB}`, and `${DOCKER_REDIS_URL}`, and mounted `./evaluation:/app/evaluation`.

---

## 5. Files Changed

- **Backend Core & Models:** `backend/core/config.py`, `backend/core/security.py`, `backend/core/database.py`, `backend/core/rate_limit.py`, `backend/main.py`, `backend/models/document.py`, `backend/models/schemas.py`
- **Backend Services, Tasks & Routes:** `backend/services/outbox_service.py`, `backend/services/cross_verification_service.py`, `backend/services/document_parser.py`, `backend/tasks/processing_tasks.py`, `backend/api/routes/documents.py`, `backend/api/routes/corrections.py`
- **Migrations & Docs:** `backend/alembic/versions/0007_worker_lease_and_currency.py`, `backend/alembic/versions/0008_drop_currency_default.py`, `backend/MIGRATIONS.md`, `docker-compose.yml`, `.env.example`
- **Frontend:** `frontend/app/documents/[id]/page.tsx`, `frontend/app/page.tsx`, `frontend/app/search/page.tsx`
- **Evaluation & Tests:** `evaluation/generate_dataset.py`, `evaluation/evaluate.py`, `evaluation/evaluation_report.md`, `backend/tests/test_migrations.py`, `backend/tests/test_concurrency_and_reliability.py`, `backend/tests/test_ghr_01_02_03.py`, `backend/tests/test_ghr_04_05_07_08.py`, `backend/tests/test_evaluation_suite.py`

---

## 6. Database Migration Changes

1. `0007_worker_lease_currency` (revises `0006_security_owner_scope`): adds nullable `worker_id VARCHAR(128)`, `processing_lease_until TIMESTAMP`, `last_heartbeat_at TIMESTAMP`, and index `ix_documents_processing_lease_until` on `documents`.
2. `0008_drop_currency_default` (revises `0007_worker_lease_currency`): runs `ALTER TABLE extracted_invoices ALTER COLUMN currency DROP DEFAULT` non-destructively while preserving all existing rows.

---

## 7. API Changes

- `POST /api/documents/reconcile`: now enforces `require_admin_or_internal` (`401` unauthenticated, `403` non-admin user or invalid `X-Internal-Service-Token`, `200` admin or valid internal token).
- `GET /api/documents/{id}/cross-verify/history`: now joins `documents` on `reference_document_id` and filters by `owner_id` for non-admin users.
- `PUT /api/documents/{id}/correct`: uses `model_fields_set` for `currency` so omitting or clearing currency preserves `null` instead of defaulting to `"USD"`.

---

## 8. Security Improvements

- Privileged reconciliation endpoint protected against horizontal/vertical privilege escalation (GHR-02).
- Cross-tenant reference document metadata and ID leakage prevented in cross-verification and history queries (GHR-03).
- Distributed rate-limiter keys hashed deterministically with SHA-256 (no raw API keys/IPs in Redis keys, consistent across worker processes) with atomic Lua enforcement (GHR-07).
- Hardcoded PostgreSQL credentials removed from `docker-compose.yml` (GHR-08).

---

## 9. Automated Tests Added

- `backend/tests/test_ghr_01_02_03.py` (4 tests): >15m heartbeat lease protection, expired-lease crash recovery, concurrent same-doc worker contention, `/reconcile` admin/internal auth, and cross-tenant history isolation.
- `backend/tests/test_ghr_04_05_07_08.py` (6 tests): `null` currency preservation across pipeline & edits, migration safety (`head`, behind `head`, missing revision, fail-fast lifespan), cross-process `PYTHONHASHSEED` rate-limit parity, atomic Redis rate limiting, and `docker-compose.yml` credential check.
- `backend/tests/test_evaluation_suite.py` (2 tests): 10-format dataset generation + real PyMuPDF/Tesseract/OpenCV/Pandas parsing, and metric/hallucination/line-item F1 calculation verification.

---

## 10. Actual Test Execution & Benchmark Results

- **Alembic Current Revision:** `0008_drop_currency_default (head)`
- **Full Backend Test Suite (`docker compose exec backend pytest tests/ -v`):**
  - **`77 passed, 1 warning in 16.19s`** (`test_ghr_01_02_03.py`: 4 passed; `test_ghr_04_05_07_08.py`: 6 passed + `test_migrations.py`: 3 passed; `test_evaluation_suite.py`: 2 passed; all 62 prior tests passed).
- **Live 10-Document End-to-End Evaluation (`docker compose exec backend python /app/evaluation/evaluate.py --delay 1.5`):**
  - Processing Success / Failure Rate: **`100.00% (10/10)`** / **`0.00% (0/10)`**
  - Overall Scalar Field Accuracy: **`88.75%`** (`invoice_number`: 90%, `invoice_date`: 90%, `supplier_name`: 90%, `customer_name`: 80%, `subtotal`: 90%, `tax`: 90%, `total_amount`: 90%, `currency`: 90%)
  - Line-Item Precision / Recall / F1: **`100.00% / 96.55% / 98.25%`** (Exact doc match: `90.00%`)
  - Arithmetic Consistency / Discrepancy Detection: **`100.00% (9/9)`** / **`100.00% (1/1)`**
  - Hallucination Rate (on 4 null truth fields): **`0.00% (0/4)`**
  - Average Latency: Parse/OCR `0.62s`, AI `1.48s`, Total **`2.10 sec/doc`**

---

## 11. Frontend Build Results

- Command: `cd frontend && npm run build && cd ..`
- Output: `✓ Compiled successfully`, `✓ Linting and checking validity of types`, `Generating static pages (5/5)` (`/`, `/_not-found`, `/documents/[id]`, `/search`).

---

## 12. Remaining Known Limitations

1. **Heavily Degraded Low-Contrast Skewed Scans (`doc_04`):** In the benchmark, `doc_04` (2.5° skew + Gaussian noise + low contrast + Gaussian blur) yielded unreadable OCR output leading to `0/8` extracted fields. `doc_06` (degraded JPG) had 1 OCR character substitution (`Greenfieid` vs `Greenfield`), yielding `7/8`.
2. **Dataset Size & `.xls` Coverage:** The reproducible benchmark contains 10 synthetic multi-format fixtures (including 12-page PDF, 2-page scanned PDF, PNG, JPG, multi-sheet XLSX, CSV, incomplete & discrepancy PDFs) rather than 100+ proprietary real-world vendor invoices; legacy `.xls` parsing is covered in unit tests via `xlrd`.
3. **Production Scale (1,000-page PDF):** Page streaming and removal of the 15-page cap are implemented, and a 12-page multi-page PDF was benchmarked (`0.00s` parse, `2.57s` AI, `100%` items F1), while full 1,000-page binary PDF wall-clock/RSS benchmarking remains for Phase 6 / production capacity testing.

---

## 13. Manual Verification Steps

1. Run `docker compose up -d` and confirm all 4 containers (`postgres`, `redis`, `backend`, `celery_worker`) are healthy.
2. Run `docker compose exec backend alembic current` -> confirm `0008_drop_currency_default (head)`.
3. Run `docker compose exec backend pytest tests/ -v` -> confirm `77 passed`.
4. Run `docker compose exec backend python /app/evaluation/evaluate.py --delay 1.5` and inspect `evaluation/evaluation_report.md`.
5. Run `cd frontend && npm run build && cd ..` -> confirm clean TypeScript compilation and static/dynamic route build.

---

## 14. Confirmation on Honesty of Claims

All metrics, latencies, accuracy figures, and test counts in this report come directly from observed tool outputs (`pytest`, `next build`, `alembic current`, and `evaluation/evaluate.py`). Failures and OCR degradation (`doc_04`: `0/8`, `doc_06`: `7/8`) are reported candidly without inflation or fabrication.
