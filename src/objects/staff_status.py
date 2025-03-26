from typing import Annotated, Any, Dict, List

from pydantic import BaseModel, StringConstraints
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import StaffStatus as StaffStatusTable

from .abstract_object import AbstrackPesopolisObject


class StaffStatusModel(BaseModel):
    id: int | None = None
    name: Annotated[str, StringConstraints(max_length=255)]
    big_dog_price: float
    low_dog_price: float
    group_price: float


class StaffStatus(AbstrackPesopolisObject):
    _table_class = StaffStatusTable
    _model_class = StaffStatusModel

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        data: Dict[str, Any],
        from_other_object: bool = False,
    ) -> Dict[str, int]:
        return await super(StaffStatus, cls).create(session, data, from_other_object)

    @classmethod
    async def create_many(
        cls,
        session: AsyncSession,
        data: List[Dict[str, Any]],
        from_other_object: bool = False,
    ) -> Dict[str, List[int]]:
        return await super(StaffStatus, cls).create_many(
            session, data, from_other_object
        )

    @classmethod
    async def get(
        cls, session: AsyncSession, data: Dict[str, Any] | None
    ) -> List[Dict[str, Any]]:
        return await super(StaffStatus, cls).get(session, data)

    @classmethod
    async def get_one(
        cls, session: AsyncSession, object_id: int, data: Dict[str, Any] | None
    ) -> Dict[str, Any]:
        return await super(StaffStatus, cls).get_one(session, object_id, data)

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        object_id: int,
        data: Dict[str, Any],
        from_other_object: bool = False,
    ) -> Dict[str, Any]:
        return await super(StaffStatus, cls).update(
            session, object_id, data, from_other_object
        )

    @classmethod
    async def update_many(
        cls,
        session: AsyncSession,
        data: List[Dict[str, Any]],
        from_other_object: bool = False,
    ) -> Dict[str, List[int]]:
        return await super(StaffStatus, cls).update_many(
            session, data, from_other_object
        )

    @classmethod
    async def delete(
        cls, session: AsyncSession, object_id: int, from_other_object: bool = False
    ) -> Dict[str, Any]:
        return await super(StaffStatus, cls).delete(
            session, object_id, from_other_object
        )

    @classmethod
    async def delete_many(
        cls,
        session: AsyncSession,
        object_ids: List[int],
        from_other_object: bool = False,
    ) -> Dict[str, List[int]]:
        return await super(StaffStatus, cls).delete_many(
            session, object_ids, from_other_object
        )
