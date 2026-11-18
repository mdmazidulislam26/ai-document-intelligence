# Security Architecture & Remaining Production Requirements

## Implemented Controls (Phase 5.1 Task 9)
1. **Explicit CORS Policy:** Removed wildcard origin regex; `CORSMiddleware` restricts origins to `settings.get_allowed_origins()` (with explicit Codespaces frontend port computation when `CODESPACE_NAME` is set).
2. **Authentication & Owner-Scoped Authorization:**
   - All document and search endpoints require either `X-API-Key` (constant-time `hmac.compare_digest` verification) or an HMAC-SHA256 signed `Authorization: Bearer <token>` issued via `POST /api/auth/token`.
   - Every `Document` is bound to `owner_id`. Cross-tenant reads, corrections, reprocessing, cross-verifications, and both search branches (GIN FTS + pgvector HNSW) strictly enforce `owner_id` filtering.
   - Production mode (`ENVIRONMENT=production`) fails closed if `API_KEYS_JSON` or `AUTH_SECRET_KEY` is unconfigured.
3. **Upload & Archive Hardening:**
   - Streaming chunked size enforcement (HTTP 413) and `MAX_FILES_PER_UPLOAD` limit.
   - Magic-byte verification, path-traversal sanitization, and `.xlsx` ZIP-bomb checks (entry count <= 1000, uncompressed <= 100MB, compression ratio <= 100:1, archive entry traversal prevention).
4. **Rate Limiting:** Redis-backed (with thread-safe in-memory fallback) sliding-window rate limiter on upload, search, and write routes returning HTTP `429` with `Retry-After`.
5. **Logging Hygiene:** Redacted raw LLM/invoice payloads from error logs.

## Remaining Scope for Full Enterprise Production
- **Full User/Identity Provider:** Replace static environment `API_KEYS_JSON` with a database-backed user table (Argon2/bcrypt password hashing) or enterprise OIDC/OAuth2/SSO (e.g., Auth0, Keycloak, Cognito).
- **Secrets Management & Key Rotation:** Store `AUTH_SECRET_KEY` and `GROQ_API_KEY` in a cloud secret manager (AWS Secrets Manager / Vault) with automated key rotation.
- **TLS/HTTPS & Malware Scanning:** Terminate TLS at reverse proxy/load balancer and add ClamAV scanning on uploaded files before parsing.
