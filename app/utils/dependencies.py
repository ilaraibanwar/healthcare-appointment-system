# app/utils/dependencies.py
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from app.db.database import get_session

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session
