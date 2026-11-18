"""
Alembic environment configuration.
Reads SYNC_DATABASE_URL from application settings, registers ORM metadata,
and supports both CLI execution and programmatic/test connections.
"""

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
import pgvector.sqlalchemy  # noqa: F401 - register pgvector SQLAlchemy type

# Ensure backend root is importable
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from core.config import settings
from core.database import Base
import models.document  # noqa: F401 - ensure all models register on Base.metadata

config = context.config

if config.config_file_name is not None and os.path.exists(config.config_file_name):
    fileConfig(config.config_file_name, disable_existing_loggers=False)

# Inject runtime database URL safely (escape '%' for ConfigParser)
safe_sync_url = settings.SYNC_DATABASE_URL.replace("%", "%%")
config.set_main_option("sqlalchemy.url", safe_sync_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def _execute_migrations(connection) -> None:
    version_table_schema = config.attributes.get("version_table_schema", None)
    configure_kwargs = {
        "connection": connection,
        "target_metadata": target_metadata,
        "compare_type": True,
    }
    if version_table_schema:
        configure_kwargs["version_table_schema"] = version_table_schema

    context.configure(**configure_kwargs)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    provided_connection = config.attributes.get("connection", None)
    if provided_connection is not None:
        _execute_migrations(provided_connection)
        return

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        _execute_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
