import functools
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.config import DATABASE_URL, IS_TEST, TEST_DATABASE_URL

if IS_TEST:
    engine = create_async_engine(url=TEST_DATABASE_URL)
else:
    engine = create_async_engine(url=DATABASE_URL)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


def connection(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            kwargs["session"] = session
            return await func(*args, **kwargs)

    return wrapper
