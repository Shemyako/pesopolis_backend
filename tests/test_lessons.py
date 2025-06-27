from datetime import datetime
from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import bindparam

from src.config import MODULE_NAME

from .conftest import HTTP_OK


@pytest.fixture(scope="function")
def test_lesson() -> dict[str, Any]:
    return {"is_group": True, "date": "2024-01-01T12:00:00"}


@pytest.fixture(scope="function")
def test_lessons_update() -> list[dict[str, Any]]:
    return [
        {"id": 1, "is_group": False, "date": "2024-01-02T13:00:00"},
        {"id": 2, "is_group": True, "date": "2024-01-03T14:00:00"},
    ]


@pytest.fixture(scope="function")
def test_lesson_update() -> dict[str, Any]:
    return {"id": 3, "is_group": False, "date": "2024-01-04T15:00:00"}


class TestLessons:
    @pytest.mark.asyncio
    async def test_get(self, client: AsyncClient) -> None:
        response = await client.get(f"/{MODULE_NAME}/lessons/1")
        assert response.status_code == HTTP_OK

    @pytest.mark.asyncio
    async def test_create(
        self,
        client: AsyncClient,
        test_lesson: dict[str, Any],
        db_session: AsyncSession,
    ) -> None:
        response = await client.post(f"/{MODULE_NAME}/lessons", json=test_lesson)
        assert response.status_code == HTTP_OK
        assert "created_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM lessons WHERE id = :id"),
                {"id": response.json()["created_id"]},
            )
        ).first()

        assert data is not None
        assert data.is_group == test_lesson["is_group"]
        assert datetime.fromisoformat(str(data.date)) == datetime.fromisoformat(
            test_lesson["date"].replace("T", " "),
        )

    @pytest.mark.asyncio
    async def test_create_many(
        self,
        client: AsyncClient,
        test_lesson: dict[str, Any],
        db_session: AsyncSession,
    ) -> None:
        response = await client.post(
            f"/{MODULE_NAME}/lessons/many", json=[test_lesson, test_lesson]
        )
        assert response.status_code == HTTP_OK
        assert "created_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM lessons WHERE id IN :id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["created_ids"])},
            )
        ).all()

        for lesson_data in data:
            assert lesson_data.is_group == test_lesson["is_group"]
            assert datetime.fromisoformat(str(lesson_data.date)) == datetime.fromisoformat(
                test_lesson["date"].replace("T", " "),
            )

    @pytest.mark.asyncio
    async def test_update_many(
        self,
        client: AsyncClient,
        test_lessons_update: dict[str, Any],
        db_session: AsyncSession,
    ) -> None:
        response = await client.put(
            f"/{MODULE_NAME}/lessons",
            json=test_lessons_update,
        )
        assert response.status_code == HTTP_OK
        assert "updated_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM lessons WHERE id IN :id ORDER BY id").bindparams(
                    bindparam("id", expanding=True),
                ),
                {"id": tuple(response.json()["updated_ids"])},
            )
        ).all()

        for lesson_data, update_data in zip(data, test_lessons_update):
            assert lesson_data.is_group == update_data["is_group"]
            assert datetime.fromisoformat(str(lesson_data.date)) == datetime.fromisoformat(
                update_data["date"].replace("T", " "),
            )

    @pytest.mark.asyncio
    async def test_update(
        self,
        client: AsyncClient,
        test_lesson_update: dict[str, Any],
        db_session: AsyncSession,
    ) -> None:
        response = await client.put(
            f"/{MODULE_NAME}/lessons/{test_lesson_update['id']}",
            json=test_lesson_update,
        )
        assert response.status_code == HTTP_OK
        assert "updated_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM lessons WHERE id = :id"),
                {"id": response.json()["updated_id"]},
            )
        ).first()

        assert data is not None
        assert data.is_group == test_lesson_update["is_group"]
        assert datetime.fromisoformat(str(data.date)) == datetime.fromisoformat(
            test_lesson_update["date"].replace("T", " "),
        )

    @pytest.mark.asyncio
    async def test_delete_many(self, client: AsyncClient, db_session: AsyncSession) -> None:
        response = await client.request(
            method="DELETE",
            url=f"/{MODULE_NAME}/lessons",
            json=[5, 6],
        )
        assert response.status_code == HTTP_OK
        assert "deleted_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM lessons WHERE id IN :id").bindparams(
                    bindparam("id", expanding=True),
                ),
                {"id": tuple(response.json()["deleted_ids"])},
            )
        ).all()

        assert len(data) == 0

    @pytest.mark.asyncio
    async def test_delete(self, client: AsyncClient, db_session: AsyncSession) -> None:
        id_to_delete = 1
        data = (
            await db_session.execute(
                text("SELECT * FROM lessons WHERE id = :id"),
                {"id": id_to_delete},
            )
        ).first()
        assert data is not None, f"Lesson with id {id_to_delete} does not exist."

        response = await client.delete(
            f"/{MODULE_NAME}/lessons/{id_to_delete}",
        )
        assert response.status_code == HTTP_OK
        assert "deleted_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM lessons WHERE id = :id"),
                {"id": response.json()["deleted_id"]},
            )
        ).first()

        assert data is None
