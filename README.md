# AI-Powered Document Intelligence System

An enterprise-grade document intelligence system designed to ingest, extract, validate, and index financial documents (PDFs, scans, images, Excel spreadsheets, and CSVs) with schema-constrained extraction, explicit nulls for unknown fields, deterministic mathematical validation, async Celery workers, and pgvector hybrid search.

---

## 1. System Architecture

```mermaid
flowchart TD
    subgraph Client["Frontend (Next.js 14)"]
        UI[Web Dashboard]
        UploadUI[Multi-File Uploader]
        ReviewUI[Side-by-Side Review & Edit]
        SearchUI[Hybrid Search Bar]
    end

    subgraph API["FastAPI Application"]
        Router[API Gateway / Router]
        DocCtrl[Documents Controller]
        CorrCtrl[Corrections Controller]
        SearchCtrl[Search Controller]
    end

    subgraph Queue["Asynchronous Workers"]
        Redis[(Redis Message Broker)]
        Worker[Celery Worker Cluster]
    end

    subgraph Pipeline["Processing Pipeline"]
        Parser[DocumentParserService<br/>PyMuPDF + Tesseract OCR + Pandas]
        LLM[AIExtractorService<br/>Groq Free Tier - llama-3.1-8b-instant]
        Validator[DocumentValidator<br/>Decimal Reconciliation & Cross-Checks]
        Embedder[VectorService<br/>FastEmbed 384-d on Local CPU]
    end

    subgraph Storage["Persistence Layer"]
        Postgres[(PostgreSQL 16 + pgvector)]
    end

    UI --> Router
    Router --> DocCtrl & CorrCtrl & SearchCtrl
    DocCtrl -->|Transactional Outbox| Postgres
    DocCtrl -->|Post-Commit Dispatch| Redis
    Redis --> Worker
    Worker --> Parser
    Parser --> LLM
    LLM --> Validator
    Validator --> Embedder
    Embedder --> Postgres
    SearchCtrl -->|GIN FTS + HNSW Cosine RRF| Postgres
```

### Database Schema & ER Diagram (PostgreSQL 16 + pgvector)

Derived from `backend/models/document.py` and Alembic migrations `0001` through `0009`:

```mermaid
erDiagram
    DOCUMENTS ||--o| EXTRACTED_INVOICES : "has one (CASCADE)"
    DOCUMENTS ||--o{ VALIDATION_LOGS : "has many (CASCADE)"
    DOCUMENTS ||--o{ CROSS_VERIFICATION_HISTORY : "primary document_id"
    DOCUMENTS ||--o{ CROSS_VERIFICATION_HISTORY : "reference_document_id"
    DOCUMENTS ||--o{ TASK_OUTBOX : "dispatches (CASCADE)"

    DOCUMENTS {
        int id PK
        varchar owner_id "indexed, default default"
        varchar filename
        varchar file_path UK
        varchar file_type
        int file_size_bytes
        varchar status "queued|processing|validated|requires_manual_review|failed"
        text error_message
        varchar worker_id
        int lease_epoch "monotonic CAS fencing token"
        datetime processing_lease_until "indexed"
        datetime last_heartbeat_at
        datetime created_at
        datetime updated_at
    }

    EXTRACTED_INVOICES {
        int id PK
        int document_id FK "UNIQUE"
        varchar invoice_number "indexed, lower() idx"
        date invoice_date
        varchar supplier_name "indexed, lower() idx"
        varchar customer_name
        numeric subtotal "NUMERIC(12,2)"
        numeric tax "NUMERIC(12,2)"
        numeric total_amount "NUMERIC(12,2)"
        varchar currency "nullable, no default"
        jsonb line_items
        boolean is_manually_corrected
        text raw_text
        tsvector search_vector "GENERATED STORED, GIN indexed"
        vector embedding "vector(384), HNSW cosine"
    }

    VALIDATION_LOGS {
        int id PK
        int document_id FK
        varchar rule_name
        text error_description
        varchar severity "WARNING|ERROR|CRITICAL"
        datetime created_at
    }

    CROSS_VERIFICATION_HISTORY {
        int id PK
        int document_id FK
        int reference_document_id FK
        varchar verification_mode "pdf_to_pdf|pdf_to_spreadsheet"
        varchar overall_status
        int discrepancy_count
        jsonb comparison_details
        datetime created_at
    }

    TASK_OUTBOX {
        int id PK
        int document_id FK
        varchar task_name
        varchar status "pending|dispatched|completed|failed"
        int attempts
        text last_error
        datetime created_at
        datetime dispatched_at
        datetime next_attempt_at "indexed (status, next_attempt_at)"
    }
```

## 2. Key Features

  - Multi-Format Parsing: Supports digital PDFs, scanned PDFs (OpenCV deskew +
    Tesseract OCR fallback), JPG, PNG, TIFF, and multi-sheet XLSX/CSV. The
    large-PDF benchmark measures only `stream_pdf_pages()` (the page iterator),
    not OCR, the full `extract_full_text()` aggregation, or the complete AI pipeline.
      - The recorded 1,000-page parser-iterator run took 0.42 seconds
        (2,360 pages/sec; reported peak RSS 121.7 MB). This is a parser-only
        microbenchmark; For massive documents (>40,000 chars, e.g. 500–1,000 page PDFs), `DocumentParserService` streams all pages while `AIExtractorService` applies bounded head + tail window sampling (`4,500` chars each) and automatic HTTP `413` chunk-splitting to stay within Groq Free Tier TPM limits.
  - Schema-Constrained AI Extraction: Powered by Groq's llama-3.1-8b-instant
    with structured JSON output. Unknown or ambiguous fields should be null.
    In the current 10-document synthetic benchmark, 0 of 4 deliberately absent
    fields were hallucinated; this small sample does not establish a universal
    zero-hallucination guarantee.
  - Deterministic Validation Engine:
      - \sum \text{Line Items} \approx \text{Subtotal} (tolerance: 0.05).
      - \text{Subtotal} + \text{Tax} \approx \text{Total Amount}.
      - Missing field warnings and advisory-locked duplicate invoice detection
        in PostgreSQL.
      - End-to-end PDF-to-PDF and PDF-to-Excel/CSV cross-verification with
        persistent audit history (POST /api/documents/{id}/cross-verify).
  - pgvector Hybrid Search: Combines stored generated TSVECTOR Full-Text Search
    (GIN indexed) with dense semantic cosine vector search (FastEmbed
    BAAI/bge-small-en-v1.5, 384 dimensions, HNSW indexed) fused
    deterministically via Reciprocal Rank Fusion (RRF).
  - Enterprise Hardening & Reliability:
      - Worker lease fencing (lease_epoch) preventing stale workers or retries
        from overwriting state.
      - Transactional outbox with periodic Celery Beat reconciliation recovering
        broker disconnects.
      - Authentication (X-API-Key and HMAC-signed Bearer tokens) with strict
        owner_id tenant isolation across CRUD, cross-verification, and both
        search branches.
      - Strict ZIP/XLSX bomb protection, streaming 413 checks, and atomic
        distributed Redis sliding-window rate limiting.
  - Human-in-the-Loop Review UI: Side-by-side editing interface displaying
    highlighted validation errors with exact 2-decimal arithmetic
    (frontend/lib/money.ts), preserving unknown currency without false USD
    defaulting.

## 3. How to Run in GitHub Codespaces / Local Docker

Step A: Configure Environment Variables

Copy .env.example to .env and insert your free Groq API key:

cp .env.example .env

(Get a 100% free key from console.groq.com/keys and paste it into GROQ_API_KEY).

Step B: Start Infrastructure & Apply Migrations (Docker)

Start the PostgreSQL + pgvector, Redis, FastAPI, and Celery worker services:

docker compose up -d --build

Verify all 4 containers are healthy:

docker compose ps
docker compose exec backend alembic current

(Expected head revision: 0009_lease_epoch_fencing).

Step C: Run Automated Tests

Run the full backend test suite inside the container and use the actual pytest summary as the test result.

docker compose exec backend pytest tests/ -v

Step D: Run Evaluation & Large-PDF Benchmarks

Run the empirical 10-document multi-format evaluation and the 1,000-page
capacity benchmark:

docker compose exec backend python /app/evaluation/evaluate.py --delay 1.5
cat evaluation/evaluation_report.md

docker compose exec backend python /app/evaluation/benchmark_large_pdf.py
cat evaluation/large_pdf_benchmark_report.md

Step E: Start Frontend (Next.js)

Open a new terminal tab and run:

cd frontend
npm install
npm run dev

To verify the production build:

cd frontend && npm run build

## 4. Production Deployment Safety

In production, configure strong random secrets and use the hardened production configuration. The dedicated `migrate` service runs `alembic upgrade head`; the API and worker wait for that one-shot service to complete successfully.

```bash
# Back up the database using the configured production credentials
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec postgres sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' > backup.sql

# Validate the fully merged production configuration before deployment
docker compose -f docker-compose.yml -f docker-compose.prod.yml config

# Start the production stack (including the migration service)
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# Verify service and migration status
docker compose -f docker-compose.yml -f docker-compose.prod.yml ps
docker compose -f docker-compose.yml -f docker-compose.prod.yml logs migrate
```

See backend/MIGRATIONS.md and backend/SECURITY.md for full deployment guides.

## 5. REST API Endpoints & Authentication

All `/api/documents/*` and `/api/search` routes require `X-API-Key` or `Authorization: Bearer <token>`.
In Next.js development mode (`npm run dev`), the dev API key is pre-loaded; in `next start` (production mode), enter the API key in the top Navbar.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/health` | Service health & configured provider check |
| `POST` | `/api/auth/token` | Exchange `X-API-Key` for short-lived Bearer JWT |
| `POST` | `/api/documents/upload` | Multi-file upload (PDF, JPG, PNG, TIFF, XLSX, XLS, CSV) |
| `GET` | `/api/documents` | List owned documents with status & extracted results |
| `GET` | `/api/documents/{id}` | Inspect extracted fields, line items, and validation logs |
| `GET` | `/api/documents/{id}/status` | Lightweight processing status polling |
| `PUT` | `/api/documents/{id}/correct` | Manual correction, re-validation, and embedding refresh |
| `POST` | `/api/documents/{id}/reprocess` | Lease-safe requeue for failed/pending documents |
| `POST` | `/api/documents/{id}/cross-verify` | Cross-verify PDF vs PDF or PDF vs Excel/CSV |
| `GET` | `/api/documents/{id}/cross-verify/history` | View persistent cross-verification audit history |
| `POST` | `/api/documents/reconcile` | Admin/internal outbox & expired-lease reconciliation |
| `GET` | `/api/search?q=...&type=hybrid` | Keyword (GIN FTS), Semantic (pgvector HNSW), or Hybrid (RRF) search |
