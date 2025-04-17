import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# --- Custom Imports --- >
import os
import sys

# Add app directory to sys.path to allow importing app modules
# Adjust path as necessary based on where you run alembic from
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "app"))
sys.path.insert(0, APP_DIR)

from app.models.base import Base  # Import the Metadata Base
from app.models import (
    __all__ as all_models,
)  # Ensure all models are imported via __init__
from app.core.config import settings  # Import your settings

# < --- End Custom Imports ---

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Use settings for database URL --- >
# Set the sqlalchemy.url from settings instead of alembic.ini
# Ensure your settings.DATABASE_URL includes the driver, e.g., "postgresql+asyncpg://..."
if settings.DATABASE_URL:
    config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
else:
    raise ValueError("DATABASE_URL must be set in settings or environment variables")
# < --- End Use settings ---

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata  # <--- Use your Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:-
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# < --- End include_object hook ---


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Use naming convention for offline mode too
        render_as_batch=True,  # Add batch mode for SQLite compatibility if needed
        compare_type=True,  # Add compare_type for better type comparison
        # Pass the naming convention from your Base metadata
        **target_metadata.naming_convention,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,  # Add batch mode
        compare_type=True,  # Add compare_type
        # Pass the naming convention from your Base metadata
        **target_metadata.naming_convention,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.
    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
