# app/db/database.py
import os
import sys
import logging
from typing import AsyncGenerator, Optional
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
else:
    logger.warning("DATABASE_URL not set — falling back to SQLite ./dev.db.")
    DATABASE_URL = "sqlite+aiosqlite:///./dev.db"

try:
    engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
except Exception:
    logger.exception("Failed to create async engine for URL: %s", DATABASE_URL)
    sys.exit(1)

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)
Base = declarative_base()

async def create_tables() -> None:
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created/verified.")
    except Exception:
        logger.exception("Error while creating tables.")
        raise

async def drop_tables() -> None:
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.info("Database tables dropped.")
    except Exception:
        logger.exception("Error while dropping tables.")
        raise

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            try:
                await session.rollback()
            except Exception:
                logger.exception("Rollback failed.")
            raise
        finally:
            await session.close()
