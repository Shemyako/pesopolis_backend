from datetime import date
from typing import Annotated, Any

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, StringConstraints
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import Staff as StaffTable

from .abstract_object import AbstrackPesopolisObject


class StaffModel(BaseModel):
    id: int | None = None
    status: int
    name: Annotated[str, StringConstraints(max_length=255)]
    phone: Annotated[str | None, StringConstraints(max_length=30)] = None
    tg_id: int


class GetSalaryResponseModel(BaseModel):
    salary: float


class Staff(AbstrackPesopolisObject):
    _table_class = StaffTable
    _model_class = StaffModel

    def __init__(self, staff_id: int) -> None:
        super().__init__()
        self.id = staff_id

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

    async def get_salary(
        self,
        session: AsyncSession,
        start_date: date,
        end_date: date | None = None,
    ) -> GetSalaryResponseModel:
        query = """
            WITH data AS (
                SELECT CASE
                    WHEN l.is_group THEN s_s.group_price
                    WHEN d.is_big THEN s_s.big_dog_price
                    ELSE s_s.low_dog_price
                END price
                FROM lessons l
                JOIN lessons_staff l_s
                    ON l.id = l_s.lesson_id
                JOIN staffs s
                    ON s.id = l_s.staff_id
                JOIN staff_status s_s
                    ON s_s.id = s.status
                JOIN dogs d
                    ON l.dog_id = d.id
                WHERE l_s.staff_id = :staff_id
                    AND l.date BETWEEN :start_date AND :end_date
            )
            SELECT SUM(price)
            FROM data;
        """

        if not end_date:
            end_date = start_date + relativedelta(months=1)

        salary = (
            await session.execute(
                text(query),
                params={
                    "staff_id": self.id,
                    "start_date": start_date,
                    "end_date": end_date,
                },
            )
        ).scalar() or -1

        return GetSalaryResponseModel(salary=salary)
