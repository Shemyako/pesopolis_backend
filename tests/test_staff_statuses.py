from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import bindparam

from src.config import MODULE_NAME

from .conftest import HTTP_OK


@pytest.fixture(scope="function")
def test_staff_status() -> dict[str, Any]:
    return {
        "name": "Test Status",
        "big_dog_price": 1000,
        "low_dog_price": 800,
        "group_price": 500,
    }


@pytest.fixture(scope="function")
def test_staff_statuses_update() -> list[dict[str, Any]]:
    return [
        {
            "id": 2,
            "name": "Updated Status",
            "big_dog_price": 1100,
            "low_dog_price": 900,
            "group_price": 600,
        },
        {
            "id": 3,
            "name": "Updated Status",
            "big_dog_price": 1200,
            "low_dog_price": 950,
            "group_price": 650,
        },
    ]


@pytest.fixture(scope="function")
def test_staff_status_update() -> dict[str, Any]:
    return {
        "id": 2,
        "name": "Updated Status",
        "big_dog_price": 1300,
        "low_dog_price": 1000,
        "group_price": 700,
    }


class TestStaffStatuses:
    @pytest.mark.asyncio
    async def test_get(self, client: AsyncClient) -> None:
        response = await client.get(f"/{MODULE_NAME}/staff_statuses/1")
        assert response.status_code == HTTP_OK

    @pytest.mark.asyncio
    async def test_create(
        self, client: AsyncClient, test_staff_status: Any, db_session: AsyncSession
    ) -> None:
        response = await client.post(f"/{MODULE_NAME}/staff_statuses", json=test_staff_status)
        assert response.status_code == HTTP_OK
        assert "created_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM staff_status WHERE id = :id"),
                {"id": response.json()["created_id"]},
            )
        ).first()

        assert data is not None
        assert data.name == test_staff_status["name"]
        assert data.big_dog_price == test_staff_status["big_dog_price"]
        assert data.low_dog_price == test_staff_status["low_dog_price"]
        assert data.group_price == test_staff_status["group_price"]

    @pytest.mark.asyncio
    async def test_create_many(
        self, client: AsyncClient, test_staff_status: Any, db_session: AsyncSession
    ) -> None:
        response = await client.post(
            f"/{MODULE_NAME}/staff_statuses/many", json=[test_staff_status, test_staff_status]
        )
        assert response.status_code == HTTP_OK
        assert "created_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM staff_status WHERE id IN :id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["created_ids"])},
            )
        ).all()

        for status_data in data:
            assert status_data.name == test_staff_status["name"]
            assert status_data.big_dog_price == test_staff_status["big_dog_price"]
            assert status_data.low_dog_price == test_staff_status["low_dog_price"]
            assert status_data.group_price == test_staff_status["group_price"]

    @pytest.mark.asyncio
    async def test_update_many(
        self, client: AsyncClient, test_staff_statuses_update: Any, db_session: AsyncSession
    ) -> None:
        response = await client.put(
            f"/{MODULE_NAME}/staff_statuses",
            json=test_staff_statuses_update,
        )
        assert response.status_code == HTTP_OK
        assert "updated_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM staff_status WHERE id IN :id ORDER BY id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["updated_ids"])},
            )
        ).all()

        for status_data, update_data in zip(data, test_staff_statuses_update):
            assert status_data.id == update_data["id"]
            assert status_data.name == update_data["name"]
            assert status_data.big_dog_price == update_data["big_dog_price"]
            assert status_data.low_dog_price == update_data["low_dog_price"]
            assert status_data.group_price == update_data["group_price"]

    @pytest.mark.asyncio
    async def test_update(
        self, client: AsyncClient, test_staff_status_update: Any, db_session: AsyncSession
    ) -> None:
        response = await client.put(
            f"/{MODULE_NAME}/staff_statuses/{test_staff_status_update['id']}",
            json=test_staff_status_update,
        )
        assert response.status_code == HTTP_OK
        assert "updated_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM staff_status WHERE id = :id"),
                {"id": response.json()["updated_id"]},
            )
        ).first()

        assert data is not None
        assert data.name == test_staff_status_update["name"]
        assert data.big_dog_price == test_staff_status_update["big_dog_price"]
        assert data.low_dog_price == test_staff_status_update["low_dog_price"]
        assert data.group_price == test_staff_status_update["group_price"]

    @pytest.mark.asyncio
    async def test_delete_many(self, client: AsyncClient, db_session: AsyncSession) -> None:
        response = await client.request(
            method="DELETE",
            url=f"/{MODULE_NAME}/staff_statuses",
            json=[5, 6],
        )
        assert response.status_code == HTTP_OK
        assert "deleted_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM staff_status WHERE id IN :id").bindparams(
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
                text("SELECT * FROM staff_status WHERE id = :id"),
                {"id": id_to_delete},
            )
        ).first()
        assert data is not None, f"Staff_statuses with id {id_to_delete} does not exist."

        response = await client.delete(
            f"/{MODULE_NAME}/staff_statuses/{id_to_delete}",
        )
        assert response.status_code == HTTP_OK
        assert "deleted_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM staff_status WHERE id = :id"),
                {"id": response.json()["deleted_id"]},
            )
        ).first()

        assert data is None
