from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import bindparam

from src.config import MODULE_NAME

from .conftest import HTTP_OK


@pytest.fixture(scope="function")
def test_staff() -> dict[str, Any]:
    return {
        "name": "Test Staff",
        "tg_id": 123456789,
        "status": 1,
    }


@pytest.fixture(scope="function")
def test_staffs_update() -> list[dict[str, Any]]:
    return [
        {
            "id": 2,
            "name": "Updated Staff",
            "tg_id": 22334455,
            "status": 2,
        },
        {
            "id": 3,
            "name": "Updated Staff",
            "tg_id": 33445566,
            "status": 3,
        },
    ]


@pytest.fixture(scope="function")
def test_staff_update() -> dict[str, Any]:
    return {
        "id": 4,
        "name": "Updated Staff",
        "tg_id": 44556677,
        "status": 1,
    }


class TestStaff:
    @pytest.mark.asyncio
    async def test_get(self, client: AsyncClient) -> None:
        response = await client.get(f"/{MODULE_NAME}/staffs/1")
        assert response.status_code == HTTP_OK

    @pytest.mark.asyncio
    async def test_create(
        self, client: AsyncClient, test_staff: Any, db_session: AsyncSession
    ) -> None:
        response = await client.post(f"/{MODULE_NAME}/staffs", json=test_staff)
        assert response.status_code == HTTP_OK
        assert "created_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM staffs WHERE id = :id"),
                {"id": response.json()["created_id"]},
            )
        ).first()

        assert data is not None
        assert data.name == test_staff["name"]
        assert data.tg_id == test_staff["tg_id"]
        assert data.status == test_staff["status"]

    @pytest.mark.asyncio
    async def test_create_many(
        self, client: AsyncClient, test_staff: Any, db_session: AsyncSession
    ) -> None:
        response = await client.post(f"/{MODULE_NAME}/staffs/many", json=[test_staff, test_staff])
        assert response.status_code == HTTP_OK
        assert "created_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM staffs WHERE id IN :id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["created_ids"])},
            )
        ).all()

        for staff_data in data:
            assert staff_data.name == test_staff["name"]
            assert staff_data.tg_id == test_staff["tg_id"]
            assert staff_data.status == test_staff["status"]

    @pytest.mark.asyncio
    async def test_update_many(
        self, client: AsyncClient, test_staffs_update: Any, db_session: AsyncSession
    ) -> None:
        response = await client.put(
            f"/{MODULE_NAME}/staffs",
            json=test_staffs_update,
        )
        assert response.status_code == HTTP_OK
        assert "updated_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM staffs WHERE id IN :id ORDER BY id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["updated_ids"])},
            )
        ).all()

        for staff_data, update_data in zip(data, test_staffs_update):
            assert staff_data.name == update_data["name"]
            assert staff_data.tg_id == update_data["tg_id"]
            assert staff_data.status == update_data["status"]

    @pytest.mark.asyncio
    async def test_update(
        self, client: AsyncClient, test_staff_update: Any, db_session: AsyncSession
    ) -> None:
        response = await client.put(
            f"/{MODULE_NAME}/staffs/4",
            json=test_staff_update,
        )
        assert response.status_code == HTTP_OK
        assert "updated_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM staffs WHERE id = :id"),
                {"id": response.json()["updated_id"]},
            )
        ).first()

        assert data is not None
        assert data.name == test_staff_update["name"]
        assert data.tg_id == test_staff_update["tg_id"]
        assert data.status == test_staff_update["status"]

    @pytest.mark.asyncio
    async def test_delete_many(self, client: AsyncClient, db_session: AsyncSession) -> None:
        response = await client.request(
            method="DELETE",
            url=f"/{MODULE_NAME}/staffs",
            json=[1, 2],
        )
        assert response.status_code == HTTP_OK
        assert "deleted_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM staffs WHERE id IN :id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["deleted_ids"])},
            )
        ).all()

        assert len(data) == 0

    @pytest.mark.asyncio
    async def test_delete(self, client: AsyncClient, db_session: AsyncSession) -> None:
        response = await client.delete(
            f"/{MODULE_NAME}/staffs/1",
        )
        assert response.status_code == HTTP_OK
        assert "deleted_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM staffs WHERE id = :id"),
                {"id": response.json()["deleted_id"]},
            )
        ).first()

        assert data is None
