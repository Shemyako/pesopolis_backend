from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import bindparam

from src.config import MODULE_NAME

from .conftest import HTTP_OK


@pytest.fixture(scope="function")
def test_dog() -> dict[str, Any]:
    return {
        "name": "Test Dog",
        "breed": "Test Breed",
        "owner": 1,
        "is_big": True,
        "is_active": True,
    }


@pytest.fixture(scope="function")
def test_dogs_update() -> list[dict[str, Any]]:
    return [
        {
            "id": 2,
            "name": "Updated Dog",
            "breed": "Updated Breed",
            "owner": 2,
            "is_big": False,
            "is_active": True,
        },
        {
            "id": 3,
            "name": "Updated Dog",
            "breed": "Updated Breed",
            "owner": 3,
            "is_big": True,
            "is_active": False,
        },
    ]


@pytest.fixture(scope="function")
def test_dog_update() -> dict[str, Any]:
    return {
        "id": 4,
        "name": "Updated Dog",
        "breed": "Updated Breed",
        "owner": 4,
        "is_big": False,
        "is_active": False,
    }


class TestDogs:
    @pytest.mark.asyncio
    async def test_get(self, client: AsyncClient) -> None:
        response = await client.get(f"/{MODULE_NAME}/dogs/1")
        assert response.status_code == HTTP_OK

    @pytest.mark.asyncio
    async def test_create(
        self, client: AsyncClient, test_dog: Any, db_session: AsyncSession
    ) -> None:
        response = await client.post(f"/{MODULE_NAME}/dogs", json=test_dog)
        assert response.status_code == HTTP_OK
        assert "created_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM dogs WHERE id = :id"),
                {"id": response.json()["created_id"]},
            )
        ).first()

        assert data is not None
        assert data.name == test_dog["name"]
        assert data.breed == test_dog["breed"]
        assert data.owner == test_dog["owner"]
        assert data.is_big == test_dog["is_big"]
        assert data.is_active == test_dog["is_active"]

    @pytest.mark.asyncio
    async def test_create_many(
        self, client: AsyncClient, test_dog: Any, db_session: AsyncSession
    ) -> None:
        response = await client.post(f"/{MODULE_NAME}/dogs/many", json=[test_dog, test_dog])
        assert response.status_code == HTTP_OK
        assert "created_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM dogs WHERE id IN :id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["created_ids"])},
            )
        ).all()

        for dog_data in data:
            assert dog_data.name == test_dog["name"]
            assert dog_data.breed == test_dog["breed"]
            assert dog_data.owner == test_dog["owner"]
            assert dog_data.is_big == test_dog["is_big"]
            assert dog_data.is_active == test_dog["is_active"]

    @pytest.mark.asyncio
    async def test_update_many(
        self, client: AsyncClient, test_dogs_update: Any, db_session: AsyncSession
    ) -> None:
        response = await client.put(
            f"/{MODULE_NAME}/dogs",
            json=test_dogs_update,
        )
        assert response.status_code == HTTP_OK
        assert "updated_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM dogs WHERE id IN :id ORDER BY id").bindparams(
                    bindparam("id", expanding=True)
                ),
                {"id": tuple(response.json()["updated_ids"])},
            )
        ).all()

        for dog_data, update_data in zip(data, test_dogs_update):
            assert dog_data.name == update_data["name"]
            assert dog_data.breed == update_data["breed"]
            assert dog_data.owner == update_data["owner"]
            assert dog_data.is_big == update_data["is_big"]
            assert dog_data.is_active == update_data["is_active"]

    @pytest.mark.asyncio
    async def test_update(
        self, client: AsyncClient, test_dog_update: Any, db_session: AsyncSession
    ) -> None:
        response = await client.put(
            f"/{MODULE_NAME}/dogs/{test_dog_update['id']}",
            json=test_dog_update,
        )
        assert response.status_code == HTTP_OK
        assert "updated_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM dogs WHERE id = :id"),
                {"id": response.json()["updated_id"]},
            )
        ).first()

        assert data is not None
        assert data.name == test_dog_update["name"]
        assert data.breed == test_dog_update["breed"]
        assert data.owner == test_dog_update["owner"]
        assert data.is_big == test_dog_update["is_big"]
        assert data.is_active == test_dog_update["is_active"]

    @pytest.mark.asyncio
    async def test_delete_many(self, client: AsyncClient, db_session: AsyncSession) -> None:
        response = await client.request(
            method="DELETE",
            url=f"/{MODULE_NAME}/dogs",
            json=[5, 6],
        )
        assert response.status_code == HTTP_OK
        assert "deleted_ids" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM dogs WHERE id IN :id").bindparams(
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
                text("SELECT * FROM dogs WHERE id = :id"),
                {"id": id_to_delete},
            )
        ).first()
        assert data is not None, f"Dog with id {id_to_delete} does not exist."

        response = await client.delete(
            f"/{MODULE_NAME}/dogs/{id_to_delete}",
        )
        assert response.status_code == HTTP_OK
        assert "deleted_id" in response.json()

        data = (
            await db_session.execute(
                text("SELECT * FROM dogs WHERE id = :id"),
                {"id": response.json()["deleted_id"]},
            )
        ).first()

        assert data is None
