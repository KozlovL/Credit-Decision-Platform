from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base, declared_attr

from app.core.config import config


class PreBase:
    @declared_attr
    def __tablename__(cls) -> Any:
        """Автоматическое заполнение названия таблицы."""
        return cls.__name__.lower()  # type:ignore[attr-defined]


Base = declarative_base(cls=PreBase)

engine = create_async_engine(
    url=config.database_url,
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncGenerator[AsyncSession]:
    try:
        async with async_session() as session:
            yield session
    except:
        print("TEST_DATABASE_URL:", config.database_url)  # <- выводим перед вызовом
