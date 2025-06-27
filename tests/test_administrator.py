from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import bindparam

from src.config import MODULE_NAME, TEST_DATABASE_URL

from .conftest import HTTP_OK


@pytest.fixture(scope="function")
def test_administrator() -> dict[str, Any]:
    return {
        "name": "Test Admin",
        "tg_id": 123456789,
        "phone": "+79999999999",
    }


@pytest.fixture(scope="function")
def test_administrators_update() -> list[dict[str, Any]]:
    return [
        {
            "id": 2,
            "name": "Test AdminNEV",
            "tg_id": 123456789,
            "phone": "+79999999999",
        },
        {
            "id": 3,
            "name": "Test AdminNEV",
            "tg_id": 123456789,
            "phone": "+79999999999",
        },
    ]


@pytest.fixture(scope="function")
def test_administrator_update() -> dict[str, Any]:
    return {
        "id": 4,
        "name": "Test AdminNEV",
        "tg_id": 123456789,
        "phone": "+79999999999",
    }


class TestClassDemoInstance:
    @pytest.mark.asyncio
    async def test_get(self, client: AsyncClient) -> None:
        response = await client.get(f"/{MODULE_NAME}/administrators/1")
        assert response.status_code == HTTP_OK

    @pytest.mark.asyncio
    async def test_create(
        self, client: AsyncClient, test_administrator: Any, db_session: AsyncSession
    ) -> None:
        response = await client.post(f"/{MODULE_NAME}/administrators", json=test_administrator)
        print(response.json())
        assert response.status_code == HTTP_OK
        assert "created_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM administrators WHERE id = :id"),
                {"id": response.json()["created_id"]},
            )
        ).first()

        assert data is not None
        assert data.name == test_administrator["name"]
        assert data.tg_id == test_administrator["tg_id"]
        assert data.phone == test_administrator["phone"]

    @pytest.mark.asyncio
    async def test_create_many(
        self, client: AsyncClient, test_administrator: Any, db_session: AsyncSession
    ) -> None:
        response = await client.post(
            f"/{MODULE_NAME}/administrators/many", json=[test_administrator, test_administrator]
        )
        print(response.json())
        assert response.status_code == HTTP_OK
        assert "created_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM administrators WHERE id IN :id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["created_ids"])},
            )
        ).all()

        for admin_data in data:
            assert admin_data.name == test_administrator["name"]
            assert admin_data.tg_id == test_administrator["tg_id"]
            assert admin_data.phone == test_administrator["phone"]

    @pytest.mark.asyncio
    async def test_update_many(
        self, client: AsyncClient, test_administrators_update: Any, db_session: AsyncSession
    ) -> None:
        response = await client.put(
            f"/{MODULE_NAME}/administrators",
            json=test_administrators_update,
        )
        assert response.status_code == HTTP_OK
        assert "updated_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM administrators WHERE id IN :id ORDER BY id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["updated_ids"])},
            )
        ).all()

        for admin_data in data:
            assert admin_data.name == test_administrators_update[0]["name"]
            assert admin_data.tg_id == test_administrators_update[0]["tg_id"]
            assert admin_data.phone == test_administrators_update[0]["phone"]

    @pytest.mark.asyncio
    async def test_update(
        self, client: AsyncClient, test_administrator_update: Any, db_session: AsyncSession
    ) -> None:
        response = await client.put(
            f"/{MODULE_NAME}/administrators/4",
            json=test_administrator_update,
        )
        assert response.status_code == HTTP_OK
        assert "updated_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM administrators WHERE id = :id"),
                {"id": response.json()["updated_id"]},
            )
        ).first()

        assert data is not None
        assert data.name == test_administrator_update["name"]
        assert data.tg_id == test_administrator_update["tg_id"]
        assert data.phone == test_administrator_update["phone"]

    @pytest.mark.asyncio
    async def test_delete_many(self, client: AsyncClient, db_session: AsyncSession) -> None:
        response = await client.request(
            method="DELETE",
            url=f"/{MODULE_NAME}/administrators",
            json=[5, 6],
        )
        print(response.json())
        assert response.status_code == HTTP_OK
        assert "deleted_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM administrators WHERE id IN :id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["deleted_ids"])},
            )
        ).all()

        assert len(data) == 0

    @pytest.mark.asyncio
    async def test_delete(self, client: AsyncClient, db_session: AsyncSession) -> None:
        id_to_delete = 7
        data = (
            await db_session.execute(
                text("SELECT * FROM administrators WHERE id = :id"),
                {"id": id_to_delete},
            )
        ).first()
        assert data is not None, f"Administrator with id {id_to_delete} does not exist."

        response = await client.delete(
            f"/{MODULE_NAME}/administrators/{id_to_delete}",
        )
        assert response.status_code == HTTP_OK
        assert "deleted_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM administrators WHERE id = :id"),
                {"id": response.json()["deleted_id"]},
            )
        ).first()

        assert data is None
