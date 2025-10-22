"""
Alembic environment configuration for CollabQuiz
Supports async SQLAlchemy 2.0+
"""

import asyncio
import sys
from pathlib import Path
from logging.config import fileConfig
from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.engine import Connection

# ------------------------------------------------------------------------------
# 1️⃣ Charger la configuration et le .env à la racine du projet
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
ROOT_DIR = BASE_DIR.parent  # racine du projet
sys.path.insert(0, str(BASE_DIR))  # pour "app."
sys.path.insert(0, str(ROOT_DIR))  # pour "backend.app" si besoin

from app.config import settings  # ✅ ton fichier config.py

# ------------------------------------------------------------------------------
# 2️⃣ Alembic configuration
# ------------------------------------------------------------------------------
config = context.config

# Override sqlalchemy.url avec celle de settings (et donc du .env)
config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URL)

# Logging Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ------------------------------------------------------------------------------
# 3️⃣ Importer les métadonnées des modèles
# ------------------------------------------------------------------------------
from app.models import Base

target_metadata = Base.metadata


# ------------------------------------------------------------------------------
# 4️⃣ Fonctions de migration
# ------------------------------------------------------------------------------
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with the given connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode (async)."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Wrapper pour exécuter les migrations en mode online."""
    asyncio.run(run_async_migrations())


# ------------------------------------------------------------------------------
# 5️⃣ Lancer la bonne fonction
# ------------------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
