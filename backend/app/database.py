"""Async SQLAlchemy setup. The API runs fully in-memory; the DB layer provides the persistent
schema (alembic) and never prevents the API from starting if the database is unreachable."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_database_url

logger = logging.getLogger("learning_dna.db")

DATABASE_URL = get_database_url()

try:
    engine = create_async_engine(DATABASE_URL, echo=False, future=True)
    SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
except Exception as exc:  # e.g. driver (asyncpg/aiosqlite) not installed
    logger.warning("Could not create DB engine (%s). Running without a database.", exc)
    engine = None
    SessionLocal = None


async def get_db() -> AsyncIterator[AsyncSession]:
    if SessionLocal is None:
        raise RuntimeError("Database is not configured")
    async with SessionLocal() as session:
        yield session


async def init_db(timeout: float = 5.0) -> bool:
    """Create tables if missing. Returns False (never raises) if the DB is unreachable."""
    if engine is None:
        return False
    try:
        from app.models import Base

        async def _create() -> None:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

        await asyncio.wait_for(_create(), timeout=timeout)
        logger.info("Database ready: %s", DATABASE_URL.split("@")[-1])
        return True
    except Exception as exc:
        logger.warning("Database unavailable (%s). Continuing with in-memory store.", exc)
        return False
