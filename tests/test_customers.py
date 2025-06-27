from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import bindparam

from src.config import MODULE_NAME

from .conftest import HTTP_OK


@pytest.fixture(scope="function")
def test_customer() -> dict[str, Any]:
    return {
        "name": "Test Customer",
        "tg_id": 123456789,
        "phone": "+79998887766",
    }


@pytest.fixture(scope="function")
def test_customers_update() -> list[dict[str, Any]]:
    return [
        {
            "id": 2,
            "name": "Updated Customer",
            "tg_id": 22334455,
            "phone": "+79991112233",
        },
        {
            "id": 3,
            "name": "Updated Customer",
            "tg_id": 33445566,
            "phone": "+79992223344",
        },
    ]


@pytest.fixture(scope="function")
def test_customer_update() -> dict[str, Any]:
    return {
        "id": 4,
        "name": "Updated Customer",
        "tg_id": 44556677,
        "phone": "+79993334455",
    }


class TestCustomers:
    @pytest.mark.asyncio
    async def test_get(self, client: AsyncClient) -> None:
        response = await client.get(f"/{MODULE_NAME}/customers/1")
        assert response.status_code == HTTP_OK

    @pytest.mark.asyncio
    async def test_create(
        self, client: AsyncClient, test_customer: Any, db_session: AsyncSession
    ) -> None:
        response = await client.post(f"/{MODULE_NAME}/customers", json=test_customer)
        assert response.status_code == HTTP_OK
        assert "created_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM customers WHERE id = :id"),
                {"id": response.json()["created_id"]},
            )
        ).first()

        assert data is not None
        assert data.name == test_customer["name"]
        assert data.tg_id == test_customer["tg_id"]
        assert data.phone == test_customer["phone"]

    @pytest.mark.asyncio
    async def test_create_many(
        self, client: AsyncClient, test_customer: Any, db_session: AsyncSession
    ) -> None:
        response = await client.post(
            f"/{MODULE_NAME}/customers/many", json=[test_customer, test_customer]
        )
        assert response.status_code == HTTP_OK
        assert "created_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM customers WHERE id IN :id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["created_ids"])},
            )
        ).all()

        for customer_data in data:
            assert customer_data.name == test_customer["name"]
            assert customer_data.tg_id == test_customer["tg_id"]
            assert customer_data.phone == test_customer["phone"]

    @pytest.mark.asyncio
    async def test_update_many(
        self, client: AsyncClient, test_customers_update: Any, db_session: AsyncSession
    ) -> None:
        response = await client.put(
            f"/{MODULE_NAME}/customers",
            json=test_customers_update,
        )
        assert response.status_code == HTTP_OK
        assert "updated_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM customers WHERE id IN :id ORDER BY id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["updated_ids"])},
            )
        ).all()

        for customer_data, update_data in zip(data, test_customers_update):
            assert customer_data.name == update_data["name"]
            assert customer_data.tg_id == update_data["tg_id"]
            assert customer_data.phone == update_data["phone"]

    @pytest.mark.asyncio
    async def test_update(
        self, client: AsyncClient, test_customer_update: Any, db_session: AsyncSession
    ) -> None:
        response = await client.put(
            f"/{MODULE_NAME}/customers/4",
            json=test_customer_update,
        )
        assert response.status_code == HTTP_OK
        assert "updated_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM customers WHERE id = :id"),
                {"id": response.json()["updated_id"]},
            )
        ).first()

        assert data is not None
        assert data.name == test_customer_update["name"]
        assert data.tg_id == test_customer_update["tg_id"]
        assert data.phone == test_customer_update["phone"]

    @pytest.mark.asyncio
    async def test_delete_many(self, client: AsyncClient, db_session: AsyncSession) -> None:
        response = await client.request(
            method="DELETE",
            url=f"/{MODULE_NAME}/customers",
            json=[5, 6],
        )
        assert response.status_code == HTTP_OK
        assert "deleted_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM customers WHERE id IN :id").bindparams(
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
                text("SELECT * FROM customers WHERE id = :id"),
                {"id": id_to_delete},
            )
        ).first()
        assert data is not None, f"Customer with id {id_to_delete} does not exist."

        response = await client.delete(
            f"/{MODULE_NAME}/customers/{id_to_delete}",
        )
        assert response.status_code == HTTP_OK
        assert "deleted_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM customers WHERE id = :id"),
                {"id": response.json()["deleted_id"]},
            )
        ).first()

        assert data is None
