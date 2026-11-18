"""
Application configuration module.
Enforces strict production security and migration safety policies.
"""

import os
import json
from typing import Dict, List, Optional, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

KNOWN_INSECURE_SECRETS = {
    "dev-insecure-secret-change-in-production",
    "replace-with-strong-random-32byte-secret",
    "changeme",
    "secret",
}

KNOWN_INSECURE_INTERNAL_TOKENS = {
    "replace-with-internal-service-secret",
    "changeme",
    "internal-secret",
}

KNOWN_INSECURE_API_KEYS = {
    "dev-local-api-key-change-me",
}

KNOWN_WEAK_DB_MARKERS = (
    "postgres:postgres@",
    "change_me_strong_postgres_password",
)


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/doc_intelligence"
    SYNC_DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/doc_intelligence"
    REDIS_URL: str = "redis://localhost:6379/0"

    # Migration Safety (GHR-05): production NEVER auto-runs DDL migrations on API startup
    AUTO_RUN_MIGRATIONS: Optional[bool] = None

    LLM_PROVIDER: str = "groq"
    GROQ_API_KEY: str = ""
    LLM_MODEL: str = "llama-3.1-8b-instant"

    EMBEDDING_MODEL_NAME: str = "BAAI/bge-small-en-v1.5"
    EMBEDDING_DIMENSION: int = 384

    UPLOAD_DIR: str = "/tmp/doc_intelligence/uploads"
    MAX_UPLOAD_SIZE_MB: int = 50
    MAX_FILES_PER_UPLOAD: int = 20

    WORKER_LEASE_SECONDS: int = 300
    WORKER_HEARTBEAT_INTERVAL_SECONDS: int = 60

    AUTH_SECRET_KEY: str = "dev-insecure-secret-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    API_KEYS_JSON: str = ""
    INTERNAL_SERVICE_TOKEN: str = ""

    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_FAIL_CLOSED_IN_PROD: bool = True
    RATE_LIMIT_UPLOAD_PER_MIN: int = 20
    RATE_LIMIT_SEARCH_PER_MIN: int = 60
    RATE_LIMIT_WRITE_PER_MIN: int = 30

    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
    ]
    ALLOWED_ORIGIN_REGEX: Optional[str] = None

    @field_validator("ALLOWED_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

    def should_auto_migrate(self) -> bool:
        """
        Production ALWAYS disables automatic DDL migrations at API startup (GHR-05),
        even if AUTO_RUN_MIGRATIONS=true was inherited from .env.example.
        """
        if self.is_production():
            return False
        if self.AUTO_RUN_MIGRATIONS is not None:
            return self.AUTO_RUN_MIGRATIONS
        return True

    def validate_production_security(self) -> None:
        """
        Fails closed in production if any placeholder/weak secrets, dev API keys,
        or weak database credentials are configured.
        """
        if not self.is_production():
            return

        secret = (self.AUTH_SECRET_KEY or "").strip()
        if not secret or secret in KNOWN_INSECURE_SECRETS or len(secret) < 32:
            raise RuntimeError(
                "Insecure AUTH_SECRET_KEY in production: must be >= 32 chars and not a placeholder."
            )

        internal_tok = (self.INTERNAL_SERVICE_TOKEN or "").strip()
        if internal_tok:
            if internal_tok in KNOWN_INSECURE_INTERNAL_TOKENS or len(internal_tok) < 24:
                raise RuntimeError(
                    "Insecure INTERNAL_SERVICE_TOKEN in production: must be >= 24 chars and not a placeholder."
                )

        api_keys = self.get_api_keys()
        if not api_keys:
            raise RuntimeError("API_KEYS_JSON must configure at least one valid API key in production.")

        for k, meta in api_keys.items():
            if k in KNOWN_INSECURE_API_KEYS or len(k) < 16:
                raise RuntimeError("Insecure or development API key detected in production API_KEYS_JSON.")
            if not isinstance(meta, dict) or not str(meta.get("owner_id") or "").strip():
                raise RuntimeError("Every API key entry in API_KEYS_JSON must specify a non-empty owner_id.")

        for db_url in (self.DATABASE_URL, self.SYNC_DATABASE_URL):
            if any(marker in db_url for marker in KNOWN_WEAK_DB_MARKERS):
                raise RuntimeError("Weak or placeholder database credentials detected in production.")

    def get_allowed_origins(self) -> List[str]:
        origins = list(self.ALLOWED_ORIGINS)
        codespace_name = os.getenv("CODESPACE_NAME")
        forwarding_domain = os.getenv("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN", "app.github.dev")
        if codespace_name:
            cs_origin = f"https://{codespace_name}-3000.{forwarding_domain}"
            if cs_origin not in origins:
                origins.append(cs_origin)
        return origins

    def get_api_keys(self) -> Dict[str, Dict[str, str]]:
        if self.API_KEYS_JSON and self.API_KEYS_JSON.strip():
            parsed = json.loads(self.API_KEYS_JSON)
            if isinstance(parsed, dict):
                return parsed

        if self.ENVIRONMENT.lower() in ("development", "dev", "test"):
            return {
                "dev-local-api-key-change-me": {"owner_id": "default", "role": "user"},
            }
        return {}

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
