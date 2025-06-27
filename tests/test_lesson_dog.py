from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import bindparam

from src.config import MODULE_NAME

from .conftest import HTTP_OK


@pytest.fixture(scope="function")
def test_lesson_dog() -> dict[str, Any]:
    return {
        "lesson_id": 1,
        "dog_id": 1,
    }


@pytest.fixture(scope="function")
def test_lesson_dogs_update() -> list[dict[str, Any]]:
    return [
        {
            "id": 2,
            "lesson_id": 2,
            "dog_id": 2,
        },
        {
            "id": 3,
            "lesson_id": 3,
            "dog_id": 3,
        },
    ]


@pytest.fixture(scope="function")
def test_lesson_dog_update() -> dict[str, Any]:
    return {
        "id": 4,
        "lesson_id": 4,
        "dog_id": 4,
    }


class TestLessonDog:
    @pytest.mark.asyncio
    async def test_get(self, client: AsyncClient) -> None:
        response = await client.get(f"/{MODULE_NAME}/lesson_dog/1")
        assert response.status_code == HTTP_OK

    @pytest.mark.asyncio
    async def test_create(
        self, client: AsyncClient, test_lesson_dog: Any, db_session: AsyncSession
    ) -> None:
        response = await client.post(f"/{MODULE_NAME}/lesson_dog", json=test_lesson_dog)
        assert response.status_code == HTTP_OK
        assert "created_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM lesson_dog WHERE id = :id"),
                {"id": response.json()["created_id"]},
            )
        ).first()

        assert data
        assert data.lesson_id == test_lesson_dog["lesson_id"]
        assert data.dog_id == test_lesson_dog["dog_id"]

    @pytest.mark.asyncio
    async def test_create_many(
        self, client: AsyncClient, test_lesson_dog: Any, db_session: AsyncSession
    ) -> None:
        response = await client.post(
            f"/{MODULE_NAME}/lesson_dog/many", json=[test_lesson_dog, test_lesson_dog]
        )
        assert response.status_code == HTTP_OK
        assert "created_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM lesson_dog WHERE id IN :id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["created_ids"])},
            )
        ).all()

        for item in data:
            assert item.lesson_id == test_lesson_dog["lesson_id"]
            assert item.dog_id == test_lesson_dog["dog_id"]

    @pytest.mark.asyncio
    async def test_update_many(
        self, client: AsyncClient, test_lesson_dogs_update: Any, db_session: AsyncSession
    ) -> None:
        response = await client.put(
            f"/{MODULE_NAME}/lesson_dog",
            json=test_lesson_dogs_update,
        )
        assert response.status_code == HTTP_OK
        assert "updated_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM lesson_dog WHERE id IN :id ORDER BY id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["updated_ids"])},
            )
        ).all()

        for item, update in zip(data, test_lesson_dogs_update):
            assert item.lesson_id == update["lesson_id"]
            assert item.dog_id == update["dog_id"]

    @pytest.mark.asyncio
    async def test_update(
        self, client: AsyncClient, test_lesson_dog_update: Any, db_session: AsyncSession
    ) -> None:
        response = await client.put(
            f"/{MODULE_NAME}/lesson_dog/{test_lesson_dog_update['id']}",
            json=test_lesson_dog_update,
        )
        assert response.status_code == HTTP_OK
        assert "updated_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM lesson_dog WHERE id = :id"),
                {"id": response.json()["updated_id"]},
            )
        ).first()

        assert data
        assert data.lesson_id == test_lesson_dog_update["lesson_id"]
        assert data.dog_id == test_lesson_dog_update["dog_id"]

    @pytest.mark.asyncio
    async def test_delete_many(self, client: AsyncClient, db_session: AsyncSession) -> None:
        response = await client.request(
            method="DELETE",
            url=f"/{MODULE_NAME}/lesson_dog",
            json=[1, 2],
        )
        assert response.status_code == HTTP_OK
        assert "deleted_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM lesson_dog WHERE id IN :id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["deleted_ids"])},
            )
        ).all()

        assert len(data) == 0

    @pytest.mark.asyncio
    async def test_delete(self, client: AsyncClient, db_session: AsyncSession) -> None:
        response = await client.delete(
            f"/{MODULE_NAME}/lesson_dog/1",
        )
        assert response.status_code == HTTP_OK
        assert "deleted_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM lesson_dog WHERE id = :id"),
                {"id": response.json()["deleted_id"]},
            )
        ).first()

        assert data is None
