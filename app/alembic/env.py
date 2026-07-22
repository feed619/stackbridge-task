import asyncio
from logging.config import fileConfig
import os
import sys

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from app.database.models import Base

from config import settings

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.get_database_url())
target_metadata = Base.metadata


def get_async_engine():
    """Create and return an asynchronous SQLAlchemy engine."""
    return create_async_engine(settings.get_database_url(), poolclass=pool.NullPool)


async def run_migrations_online():
    """Run migrations in 'online' mode (with an active database connection)."""
    connectable = get_async_engine()

    async with connectable.connect() as connection:
        # Pass the migration function to run_sync (no await inside)
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    """Configure Alembic context and execute migrations."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_offline():
    """Run migrations in 'offline' mode (without a real database connection)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
