from typing import Annotated, Any, Dict, List

from pydantic import BaseModel, StringConstraints
from sqlalchemy.ext.asyncio import AsyncSession

from db import Staff as StaffTable

from .abstract_object import AbstrackPesopolisObject


class StaffModel(BaseModel):
    id: int | None = None
    status: int
    name: Annotated[str, StringConstraints(max_length=255)]
    phone: Annotated[str | None, StringConstraints(max_length=30)] = None
    tg_id: int


class Staff(AbstrackPesopolisObject):
    _table_class = StaffTable
    _model_class = StaffModel

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        data: Dict[str, Any],
        from_other_object: bool = False,
    ) -> Dict[str, int]:
        return await super(Staff, cls).create(session, data, from_other_object)

    @classmethod
    async def create_many(
        cls,
        session: AsyncSession,
        data: List[Dict[str, Any]],
        from_other_object: bool = False,
    ) -> Dict[str, List[int]]:
        return await super(Staff, cls).create_many(session, data, from_other_object)

    @classmethod
    async def get(
        cls, session: AsyncSession, data: Dict[str, Any] | None
    ) -> List[Dict[str, Any]]:
        return await super(Staff, cls).get(session, data)

    @classmethod
    async def get_one(
        cls, session: AsyncSession, object_id: int, data: Dict[str, Any] | None
    ) -> Dict[str, Any]:
        return await super(Staff, cls).get_one(session, object_id, data)

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        object_id: int,
        data: Dict[str, Any],
        from_other_object: bool = False,
    ) -> Dict[str, Any]:
        return await super(Staff, cls).update(
            session, object_id, data, from_other_object
        )

    @classmethod
    async def update_many(
        cls,
        session: AsyncSession,
        data: List[Dict[str, Any]],
        from_other_object: bool = False,
    ) -> Dict[str, List[int]]:
        return await super(Staff, cls).update_many(session, data, from_other_object)

    @classmethod
    async def delete(
        cls, session: AsyncSession, object_id: int, from_other_object: bool = False
    ) -> Dict[str, Any]:
        return await super(Staff, cls).delete(session, object_id, from_other_object)

    @classmethod
    async def delete_many(
        cls,
        session: AsyncSession,
        object_ids: List[int],
        from_other_object: bool = False,
    ) -> Dict[str, List[int]]:
        return await super(Staff, cls).delete_many(
            session, object_ids, from_other_object
        )
