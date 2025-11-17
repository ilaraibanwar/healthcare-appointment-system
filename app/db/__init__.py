# app/db/__init__.py
from .database import engine, Base, get_session, create_tables, drop_tables, AsyncSessionLocal
from . import models

async def create_tables_async():
    await create_tables()

def create_tables_sync():
    import asyncio
    asyncio.run(create_tables_async())
