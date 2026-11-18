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

2. Key Features

  - Multi-Format Parsing: Supports digital PDFs, scanned PDFs (OpenCV deskew +
    Tesseract OCR fallback), JPG, PNG, TIFF, and multi-sheet XLSX/CSV. The
    large-PDF benchmark measures only `stream_pdf_pages()` (the page iterator),
    not OCR, the full `extract_full_text()` aggregation, or the complete AI pipeline.
      - The recorded 1,000-page parser-iterator run took 0.42 seconds
        (2,360 pages/sec; reported peak RSS 121.7 MB). This is a parser-only
        microbenchmark, not an end-to-end 1,000-page processing guarantee.
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

3. How to Run in GitHub Codespaces / Local Docker

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

4. Production Deployment Safety

In production, configure strong random secrets and use the hardened production configuration. The dedicated `migrate` service runs `alembic upgrade head`; the API and worker wait for that one-shot service to complete successfully.

```bash
# Back up the database using the configured production credentials
docker compose exec postgres sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' > backup.sql

# Validate the fully merged production configuration before deployment
docker compose -f docker-compose.yml -f docker-compose.prod.yml config

# Start the production stack (including the migration service)
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# Verify service and migration status
docker compose -f docker-compose.yml -f docker-compose.prod.yml ps
docker compose -f docker-compose.yml -f docker-compose.prod.yml logs migrate
```

See backend/MIGRATIONS.md and backend/SECURITY.md for full deployment guides.
