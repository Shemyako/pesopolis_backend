from collections.abc import AsyncGenerator

import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.engine import Connection as SyncConnection
from sqlalchemy.engine import Transaction as SyncTransaction
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.app import create_application
from src.config import TEST_DATABASE_URL
from src.db.database import Base, get_session


@pytest_asyncio.fixture(scope="session")
async def async_engine() -> AsyncEngine:
    """Создание асинхронного движка БД для тестов."""
    return create_async_engine(TEST_DATABASE_URL, future=True, echo=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db(async_engine: AsyncEngine) -> AsyncGenerator[None, None]:
    """Создание БД для тестов."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def db_session(async_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Фикстура для создания сессии БД для тестов."""
    async_session = async_sessionmaker(async_engine, expire_on_commit=False)

    async with async_engine.connect() as conn:
        trans = await conn.begin()

        session = async_session(bind=conn)

        # savepoint
        await conn.begin_nested()

        @event.listens_for(session.sync_session, "after_transaction_end")
        def restart_savepoint(
            conn_: SyncConnection,
            transaction_: SyncTransaction,
        ) -> None:
            if transaction_.nested and not transaction_._parent.nested:
                conn_.begin_nested()

        try:
            yield session
        finally:
            await session.close()
            await trans.rollback()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepopulate_db(async_engine: AsyncEngine) -> None:
    """Заполнение БД тестовыми данными перед всеми тестами."""
    from src.db.models import CourseToDog

    from .data_test import (
        test_admins,
        test_cources,
        test_customers,
        test_dogs,
        test_lesson_dog,
        test_lesson_staff,
        test_lessons,
        test_staff,
        test_staff_statuses,
    )

    async_session = async_sessionmaker(async_engine, expire_on_commit=False)
    async with async_session() as session:
        session.add_all(
            test_admins + test_cources + test_customers + test_staff_statuses + test_lessons
        )
        await session.flush()

        for i, dog in enumerate(test_dogs):
            dog.owner = test_customers[i].id
        session.add_all(test_dogs)
        await session.flush()

        dog_to_cource = [
            CourseToDog(dog_id=dog.id, course_id=test_cources[0].id) for dog in test_dogs
        ]
        session.add_all(dog_to_cource)
        await session.flush()

        for i, staff in enumerate(test_staff):
            staff.status = test_staff_statuses[i % len(test_staff_statuses)].id
        session.add_all(test_staff)
        await session.flush()

        for ld in test_lesson_dog:
            ld.dog_id = ld.dog_id.id
            ld.lesson_id = ld.lesson_id.id

        for ls in test_lesson_staff:
            ls.staff_id = ls.staff_id.id
            ls.lesson_id = ls.lesson_id.id
        session.add_all(test_lesson_dog + test_lesson_staff)
        await session.commit()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def override_app(db_session: AsyncSession) -> FastAPI:
    """Подмена get_session на фикстуру db_session для тестов."""
    app = create_application()

    async def _get_override_session() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_session] = _get_override_session
    return app


@pytest_asyncio.fixture(scope="function")
async def client(override_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Фикстура для создания клиента HTTP для тестов."""
    async with AsyncClient(
        transport=ASGITransport(override_app),
        base_url="http://localhost",
    ) as ac:
        yield ac


HTTP_OK = 200
