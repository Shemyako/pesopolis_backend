from typing import Annotated, Any, Dict, List

from pydantic import BaseModel, StringConstraints
from sqlalchemy.ext.asyncio import AsyncSession

from db import Cource as CourseTable

from .abstract_object import AbstrackPesopolisObject


class CourseModel(BaseModel):
    id: int | None = None
    name: Annotated[str, StringConstraints(max_length=255)]
    lessons_amount: int
    price: float


class Course(AbstrackPesopolisObject):
    _table_class = CourseTable
    _model_class = CourseModel

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        data: Dict[str, Any],
        from_other_object: bool = False,
    ) -> Dict[str, int]:
        return await super(Course, cls).create(session, data, from_other_object)

    @classmethod
    async def create_many(
        cls,
        session: AsyncSession,
        data: List[Dict[str, Any]],
        from_other_object: bool = False,
    ) -> Dict[str, List[int]]:
        return await super(Course, cls).create_many(session, data, from_other_object)

    @classmethod
    async def get(
        cls, session: AsyncSession, data: Dict[str, Any] | None
    ) -> List[Dict[str, Any]]:
        return await super(Course, cls).get(session, data)

    @classmethod
    async def get_one(
        cls, session: AsyncSession, object_id: int, data: Dict[str, Any] | None
    ) -> Dict[str, Any]:
        return await super(Course, cls).get_one(session, object_id, data)

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        object_id: int,
        data: Dict[str, Any],
        from_other_object: bool = False,
    ) -> Dict[str, Any]:
        return await super(Course, cls).update(
            session, object_id, data, from_other_object
        )

    @classmethod
    async def update_many(
        cls,
        session: AsyncSession,
        data: List[Dict[str, Any]],
        from_other_object: bool = False,
    ) -> Dict[str, List[int]]:
        return await super(Course, cls).update_many(session, data, from_other_object)

    @classmethod
    async def delete(
        cls, session: AsyncSession, object_id: int, from_other_object: bool = False
    ) -> Dict[str, Any]:
        return await super(Course, cls).delete(session, object_id, from_other_object)

    @classmethod
    async def delete_many(
        cls,
        session: AsyncSession,
        object_ids: List[int],
        from_other_object: bool = False,
    ) -> Dict[str, List[int]]:
        return await super(Course, cls).delete_many(
            session, object_ids, from_other_object
        )
