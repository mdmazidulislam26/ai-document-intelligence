"""
Application configuration module.
Loads settings from environment variables using Pydantic Settings.
"""

import os
from typing import List, Union
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

    # Allowed CORS Origins
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000"
    ]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

# Ensure local upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
