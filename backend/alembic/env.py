import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.db.base import Base

import app.models.user
import app.models.bookings
import app.models.houses

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_online() -> None:
    async def _run() -> None:
        connectable = create_async_engine(
            settings.DB_URL,
            poolclass=pool.NullPool,
        )

        async with connectable.connect() as connection:

            def do_migrations(conn):
                context.configure(
                    connection=conn,
                    target_metadata=target_metadata,
                    compare_type=True,
                )
                with context.begin_transaction():
                    context.run_migrations()

            await connection.run_sync(do_migrations)

        await connectable.dispose()

    asyncio.run(_run())

def run_migrations_offline() -> None:
    context.configure(
        url=settings.DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()




if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
