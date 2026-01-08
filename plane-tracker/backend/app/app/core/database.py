from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.airport_model import Airport
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL
# 1. Adapt DATABASE_URL for the async driver (aiosqlite)=
# 2. Create an async engine
#    connect_args is still needed for SQLite.
#    echo=True logs SQL statements, useful for debugging.
engine = create_async_engine(DATABASE_URL, echo=True)

async def init_db():
    """
    Initializes the database and creates tables.
    This should be called on FastAPI application startup.
    For now this options is disabled.
    """
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all) # Use this to drop tables for a fresh start
        await conn.run_sync(SQLModel.metadata.create_all)

async def close_db():
    # This closes all connections in the pool
    await engine.dispose()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency to get an async database session.
    Yields a session and ensures it's closed after the request is handled.
    """
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
