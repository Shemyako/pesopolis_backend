from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import bindparam

from src.config import MODULE_NAME

from .conftest import HTTP_OK


@pytest.fixture(scope="function")
def test_lesson_staff() -> dict[str, Any]:
    return {
        "lesson_id": 1,
        "staff_id": 1,
    }


@pytest.fixture(scope="function")
def test_lesson_staffs_update() -> list[dict[str, Any]]:
    return [
        {
            "id": 2,
            "lesson_id": 2,
            "staff_id": 2,
        },
        {
            "id": 3,
            "lesson_id": 3,
            "staff_id": 3,
        },
    ]


@pytest.fixture(scope="function")
def test_lesson_staff_update() -> dict[str, Any]:
    return {
        "id": 3,
        "lesson_id": 4,
        "staff_id": 4,
    }


class TestLessonStaff:
    @pytest.mark.asyncio
    async def test_get(self, client: AsyncClient) -> None:
        response = await client.get(f"/{MODULE_NAME}/lesson_staff/1")
        assert response.status_code == HTTP_OK

    @pytest.mark.asyncio
    async def test_create(
        self, client: AsyncClient, test_lesson_staff: Any, db_session: AsyncSession
    ) -> None:
        response = await client.post(f"/{MODULE_NAME}/lesson_staff", json=test_lesson_staff)
        assert response.status_code == HTTP_OK
        assert "created_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM lesson_staff WHERE id = :id"),
                {"id": response.json()["created_id"]},
            )
        ).first()

        assert data
        assert data.lesson_id == test_lesson_staff["lesson_id"]
        assert data.staff_id == test_lesson_staff["staff_id"]

    @pytest.mark.asyncio
    async def test_create_many(
        self, client: AsyncClient, test_lesson_staff: Any, db_session: AsyncSession
    ) -> None:
        response = await client.post(
            f"/{MODULE_NAME}/lesson_staff/many", json=[test_lesson_staff, test_lesson_staff]
        )
        assert response.status_code == HTTP_OK
        assert "created_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM lesson_staff WHERE id IN :id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["created_ids"])},
            )
        ).all()

        for item in data:
            assert item.lesson_id == test_lesson_staff["lesson_id"]
            assert item.staff_id == test_lesson_staff["staff_id"]

    @pytest.mark.asyncio
    async def test_update_many(
        self, client: AsyncClient, test_lesson_staffs_update: Any, db_session: AsyncSession
    ) -> None:
        response = await client.put(
            f"/{MODULE_NAME}/lesson_staff",
            json=test_lesson_staffs_update,
        )
        assert response.status_code == HTTP_OK
        assert "updated_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM lesson_staff WHERE id IN :id ORDER BY id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["updated_ids"])},
            )
        ).all()

        for item, update in zip(data, test_lesson_staffs_update):
            assert item.lesson_id == update["lesson_id"]
            assert item.staff_id == update["staff_id"]

    @pytest.mark.asyncio
    async def test_update(
        self, client: AsyncClient, test_lesson_staff_update: Any, db_session: AsyncSession
    ) -> None:
        response = await client.put(
            f"/{MODULE_NAME}/lesson_staff/{test_lesson_staff_update['id']}",
            json=test_lesson_staff_update,
        )
        assert response.status_code == HTTP_OK
        assert "updated_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM lesson_staff WHERE id = :id"),
                {"id": response.json()["updated_id"]},
            )
        ).first()

        assert data
        assert data.lesson_id == test_lesson_staff_update["lesson_id"]
        assert data.staff_id == test_lesson_staff_update["staff_id"]

    @pytest.mark.asyncio
    async def test_delete_many(self, client: AsyncClient, db_session: AsyncSession) -> None:
        response = await client.request(
            method="DELETE",
            url=f"/{MODULE_NAME}/lesson_staff",
            json=[1, 2],
        )
        assert response.status_code == HTTP_OK
        assert "deleted_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM lesson_staff WHERE id IN :id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["deleted_ids"])},
            )
        ).all()

        assert len(data) == 0

    @pytest.mark.asyncio
    async def test_delete(self, client: AsyncClient, db_session: AsyncSession) -> None:
        response = await client.delete(
            f"/{MODULE_NAME}/lesson_staff/1",
        )
        assert response.status_code == HTTP_OK
        assert "deleted_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM lesson_staff WHERE id = :id"),
                {"id": response.json()["deleted_id"]},
            )
        ).first()

        assert data is None
