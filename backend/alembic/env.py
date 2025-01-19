import logging
import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Load the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
print(f"Loading .env from: {dotenv_path}")  # Debugging line
load_dotenv(dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set or is invalid in the .env file.")

print(f"DATABASE_URL loaded: {DATABASE_URL}")  # Debugging line

# Configure logging
if context.config.config_file_name is not None:
    fileConfig(context.config.config_file_name)

logger = logging.getLogger("alembic.runtime.migration")
logger.info("Alembic env.py is executing...")

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import models here
from backend.models.user import *
from backend.models.workout import *
from backend.models.nutrition import *
from backend.models.community_post import *
from backend.models.payment import *
from backend.models.reels import *
from backend.models.session import *

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
