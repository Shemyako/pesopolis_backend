from datetime import date

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.objects.staff import GetSalaryResponseModel, Staff

report_router = APIRouter()


class GetSalaryRequestModel(BaseModel):
    start_date: date = Field(Query())
    end_date: date | None = Field(Query(default=None))


@report_router.get("/staff/{staff_id}/salary")
async def get_salary(
    staff_id: int,
    query_data: GetSalaryRequestModel = Depends(),
    session: AsyncSession = Depends(get_session),
) -> GetSalaryResponseModel:
    staff_class = Staff(staff_id)
    res = await staff_class.get_salary(
        session, start_date=query_data.start_date, end_date=query_data.end_date
    )
    return res
