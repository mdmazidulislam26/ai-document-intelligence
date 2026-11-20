# Database Migrations, Safety Verification & Rollback Guide (Alembic)

This project uses **Alembic** for deterministic, non-destructive PostgreSQL schema management.

## 1. Startup Migration Safety Policy
- **Production (`ENVIRONMENT=production` or `AUTO_RUN_MIGRATIONS=false`):**
  - The API refuses to start (`MigrationSafetyError`) if the database has unapplied migrations, is behind `head`, or has an unknown/missing Alembic revision.
  - `Base.metadata.create_all()` is **never** relied upon in production.
- **Development (`ENVIRONMENT=development`):**
  - `init_db()` acquires a PostgreSQL advisory lock (`pg_advisory_lock`), applies `alembic upgrade head`, and verifies the schema is at `head`. Errors are never swallowed silently.

## 2. Production Deployment Workflow
1. **Back up the database before upgrading:**
   ```bash
   docker compose exec postgres pg_dump -U "${POSTGRES_USER:-postgres}" "${POSTGRES_DB:-doc_intelligence}" > backup_before_migration.sql
   ```
2. **Apply pending migrations:**
   ```bash
   docker compose exec backend alembic upgrade head
   ```
3. **Verify current revision matches `head`:**
   ```bash
   docker compose exec backend alembic current
   docker compose exec backend alembic heads
   ```
4. **Start/restart API and worker services.**

## 3. Creating Future Migrations
Whenever `backend/models/document.py` is updated:
```bash
docker compose exec backend alembic revision --autogenerate -m "describe_change"
```
Always inspect the generated script in `backend/alembic/versions/` before applying it.

## 4. Rollback Procedure
- **Rollback one revision safely:**
  ```bash
  docker compose exec backend alembic downgrade -1
  ```
- **Inspect migration history:**
  ```bash
  docker compose exec backend alembic history --verbose
  ```
