# Database Migrations & Rollback Guide (Alembic)

This project uses **Alembic** for deterministic, non-destructive PostgreSQL schema management.

## 1. Fresh Database Initialization
When starting with `docker compose up -d --build`, the `backend` container automatically runs:
```bash
alembic upgrade head