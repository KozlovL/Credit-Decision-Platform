from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import declared_attr, declarative_base

from app.core.config import config


class PreBase:
    @declared_attr
    def __tablename__(cls):
        """Автоматическое заполнение названия таблицы."""
        return cls.__name__.lower()


Base = declarative_base(cls=PreBase)

engine = create_async_engine(
    url=config.database_url,
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session
