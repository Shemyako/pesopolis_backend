from typing import Annotated, Any

from pydantic import BaseModel, StringConstraints
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import Administrator as AdministratorTable

from .abstract_object import AbstrackPesopolisObject


class AdministratorModel(BaseModel):
    id: int | None = None
    name: Annotated[str, StringConstraints(max_length=255)]
    phone: Annotated[str | None, StringConstraints(max_length=30)] = None
    tg_id: int


class Administrator(AbstrackPesopolisObject):
    _table_class = AdministratorTable
    _model_class = AdministratorModel

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        data: dict[str, Any],
        from_other_object: bool = False,
    ) -> dict[str, int]:
        return await super().create(session, data, from_other_object)

    @classmethod
    async def create_many(
        cls,
        session: AsyncSession,
        data: list[dict[str, Any]],
        from_other_object: bool = False,
    ) -> dict[str, list[int]]:
        return await super().create_many(session, data, from_other_object)

    @classmethod
    async def get(cls, session: AsyncSession, data: dict[str, Any] | None) -> list[dict[str, Any]]:
        return await super().get(session, data)

    @classmethod
    async def get_one(
        cls, session: AsyncSession, object_id: int, data: dict[str, Any] | None
    ) -> dict[str, Any]:
        return await super().get_one(session, object_id, data)

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        object_id: int,
        data: dict[str, Any],
        from_other_object: bool = False,
    ) -> dict[str, Any]:
        return await super().update(session, object_id, data, from_other_object)

    @classmethod
    async def update_many(
        cls,
        session: AsyncSession,
        data: list[dict[str, Any]],
        from_other_object: bool = False,
    ) -> dict[str, list[int]]:
        return await super().update_many(session, data, from_other_object)

    @classmethod
    async def delete(
        cls, session: AsyncSession, object_id: int, from_other_object: bool = False
    ) -> dict[str, Any]:
        return await super().delete(session, object_id, from_other_object)

    @classmethod
    async def delete_many(
        cls,
        session: AsyncSession,
        object_ids: list[int],
        from_other_object: bool = False,
    ) -> dict[str, list[int]]:
        return await super().delete_many(session, object_ids, from_other_object)
