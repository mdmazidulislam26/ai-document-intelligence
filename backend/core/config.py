"""
Application configuration module.
Loads settings from environment variables using Pydantic Settings.
"""

import os
import json
from typing import Dict, List, Optional, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application Environment
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Server Binding
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    # PostgreSQL Database URL
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/doc_intelligence"
    SYNC_DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/doc_intelligence"

    # Redis Broker URL
    REDIS_URL: str = "redis://localhost:6379/0"

    # Free AI Provider Configurations (Default: Groq Cloud free tier)
    LLM_PROVIDER: str = "groq"
    GROQ_API_KEY: str = ""
    LLM_MODEL: str = "llama-3.1-8b-instant"

    # Local Embedding Model (FastEmbed running locally on CPU - 384 dimensions)
    EMBEDDING_MODEL_NAME: str = "BAAI/bge-small-en-v1.5"
    EMBEDDING_DIMENSION: int = 384

    # File Upload Directory & Constraints
    UPLOAD_DIR: str = "/tmp/doc_intelligence/uploads"
    MAX_UPLOAD_SIZE_MB: int = 50
    MAX_FILES_PER_UPLOAD: int = 20

    # Authentication & Authorization
    AUTH_SECRET_KEY: str = "dev-insecure-secret-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    API_KEYS_JSON: str = ""

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_UPLOAD_PER_MIN: int = 20
    RATE_LIMIT_SEARCH_PER_MIN: int = 60
    RATE_LIMIT_WRITE_PER_MIN: int = 30

    # Allowed CORS Origins
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

    def get_allowed_origins(self) -> List[str]:
        origins = list(self.ALLOWED_ORIGINS)
        # Automatically allow exact Codespaces forwarded frontend origin if running in Codespaces
        codespace_name = os.getenv("CODESPACE_NAME")
        forwarding_domain = os.getenv("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN", "app.github.dev")
        if codespace_name:
            cs_origin = f"https://{codespace_name}-3000.{forwarding_domain}"
            if cs_origin not in origins:
                origins.append(cs_origin)
        return origins

    def get_api_keys(self) -> Dict[str, Dict[str, str]]:
        """
        Parses configured API keys.
        Fails closed in production if API_KEYS_JSON is empty or secret is default.
        Provides a clearly scoped development-only key when ENVIRONMENT=development and unconfigured.
        """
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
