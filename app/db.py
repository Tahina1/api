from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(settings.database_url, pool_size=10, pool_pre_ping=True)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    """Parent class for all entities."""

async def get_session() -> AsyncIterator[AsyncSession]:
    """FastAPI: one session = one request, automatically closed"""
    async with SessionLocal() as session:
        yield session