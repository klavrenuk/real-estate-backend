"""Alembic environment for the real-estate backend.

The database URL is NOT hardcoded in alembic.ini — it is taken from app settings
(.env), so migrations and the application can never drift apart.
"""

import asyncio
import pkgutil
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.core.config import get_settings
from app.core.database import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Единственный источник правды по URL — настройки приложения (.env).
config.set_main_option("sqlalchemy.url", get_settings().database_url)


def import_models() -> None:
    """Импортировать все model.py из app/modules, чтобы они попали в metadata.

    Сделано автоматически, чтобы новая модель не терялась в автогенерации:
    достаточно создать app/modules/<domain>/model.py.
    """
    modules_path = Path(__file__).resolve().parents[1] / "app" / "modules"
    for module in pkgutil.walk_packages([str(modules_path)], prefix="app.modules."):
        if module.name.endswith(".model"):
            __import__(module.name)


import_models()

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Сгенерировать SQL-скрипты без подключения к БД."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
