from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import bindparam

from src.config import MODULE_NAME

from .conftest import HTTP_OK


@pytest.fixture(scope="function")
def test_cource() -> dict[str, Any]:
    return {
        "name": "Test Course",
        "lessons_amount": 12,
        "price": 1234,
    }


@pytest.fixture(scope="function")
def test_courses_update() -> list[dict[str, Any]]:
    return [
        {
            "id": 2,
            "name": "Updated Course",
            "lessons_amount": 15,
            "price": 1500,
        },
        {
            "id": 3,
            "name": "Updated Course",
            "lessons_amount": 20,
            "price": 2000,
        },
    ]


@pytest.fixture(scope="function")
def test_cource_update() -> dict[str, Any]:
    return {
        "id": 2,
        "name": "Updated Course",
        "lessons_amount": 25,
        "price": 2500,
    }


class TestCources:
    @pytest.mark.asyncio
    async def test_get(self, client: AsyncClient) -> None:
        response = await client.get(f"/{MODULE_NAME}/courses/1")
        assert response.status_code == HTTP_OK

    @pytest.mark.asyncio
    async def test_create(
        self, client: AsyncClient, test_cource: Any, db_session: AsyncSession
    ) -> None:
        response = await client.post(f"/{MODULE_NAME}/courses", json=test_cource)
        assert response.status_code == HTTP_OK
        assert "created_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM courses WHERE id = :id"),
                {"id": response.json()["created_id"]},
            )
        ).first()

        assert data is not None
        assert data.name == test_cource["name"]
        assert data.lessons_amount == test_cource["lessons_amount"]
        assert data.price == test_cource["price"]

    @pytest.mark.asyncio
    async def test_create_many(
        self, client: AsyncClient, test_cource: Any, db_session: AsyncSession
    ) -> None:
        response = await client.post(
            f"/{MODULE_NAME}/courses/many", json=[test_cource, test_cource]
        )
        assert response.status_code == HTTP_OK
        assert "created_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM courses WHERE id IN :id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["created_ids"])},
            )
        ).all()

        for cource_data in data:
            assert cource_data.name == test_cource["name"]
            assert cource_data.lessons_amount == test_cource["lessons_amount"]
            assert cource_data.price == test_cource["price"]

    @pytest.mark.asyncio
    async def test_update_many(
        self, client: AsyncClient, test_courses_update: Any, db_session: AsyncSession
    ) -> None:
        response = await client.put(
            f"/{MODULE_NAME}/courses",
            json=test_courses_update,
        )
        assert response.status_code == HTTP_OK
        assert "updated_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM courses WHERE id IN :id ORDER BY id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["updated_ids"])},
            )
        ).all()

        for cource_data, update_data in zip(data, test_courses_update):
            assert cource_data.name == update_data["name"]
            assert cource_data.lessons_amount == update_data["lessons_amount"]
            assert cource_data.price == update_data["price"]

    @pytest.mark.asyncio
    async def test_update(
        self, client: AsyncClient, test_cource_update: Any, db_session: AsyncSession
    ) -> None:
        response = await client.put(
            f"/{MODULE_NAME}/courses/{test_cource_update['id']}",
            json=test_cource_update,
        )
        assert response.status_code == HTTP_OK
        assert "updated_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM courses WHERE id = :id"),
                {"id": response.json()["updated_id"]},
            )
        ).first()

        assert data is not None
        assert data.name == test_cource_update["name"]
        assert data.lessons_amount == test_cource_update["lessons_amount"]
        assert data.price == test_cource_update["price"]

    @pytest.mark.asyncio
    async def test_delete_many(self, client: AsyncClient, db_session: AsyncSession) -> None:
        response = await client.request(
            method="DELETE",
            url=f"/{MODULE_NAME}/courses",
            json=[5, 6],
        )
        assert response.status_code == HTTP_OK
        assert "deleted_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM courses WHERE id IN :id").bindparams(
                    bindparam("id", expanding=True)
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
                text("SELECT * FROM courses WHERE id = :id"),
                {"id": id_to_delete},
            )
        ).first()
        assert data is not None, f"Cource with id {id_to_delete} does not exist."

        response = await client.delete(
            f"/{MODULE_NAME}/courses/{id_to_delete}",
        )
        assert response.status_code == HTTP_OK
        assert "deleted_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM courses WHERE id = :id"),
                {"id": response.json()["deleted_id"]},
            )
        ).first()

        assert data is None
