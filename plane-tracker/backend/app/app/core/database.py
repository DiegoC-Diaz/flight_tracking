from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# 1. Adapt DATABASE_URL for the async driver (aiosqlite)
DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"

# 2. Create an async engine
#    connect_args is still needed for SQLite.
#    echo=True logs SQL statements, useful for debugging.
engine = create_async_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

async def init_db():
    """
    Initializes the database and creates tables.
    This should be called on FastAPI application startup.
    For now this options is disabled.
    """
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all) # Use this to drop tables for a fresh start
        pass
        #await conn.run_sync(SQLModel.metadata.create_all)

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
