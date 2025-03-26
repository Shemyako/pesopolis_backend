from typing import List

import orjson
from fastapi import APIRouter, Depends, Header
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.factories import BaseFactory
from src.objects import AbstrackPesopolisObject

object_router = APIRouter()


# TODO add pydentic objects
@object_router.get("/{object_name}")
async def get_objects(
    object_name: str,
    data: str = "{}",
    session: AsyncSession = Depends(get_session),
):
    object_class: AbstrackPesopolisObject = BaseFactory.get(object_name)
    res = await object_class.get(session, orjson.loads(data))
    return ORJSONResponse(res)


@object_router.get("/{object_name}/{object_id}")
async def get_object(
    object_name: str,
    object_id: int,
    data: str = "{}",
    session: AsyncSession = Depends(get_session),
):
    object_class: AbstrackPesopolisObject = BaseFactory.get(object_name)
    res = await object_class.get_one(session, object_id, orjson.loads(data))
    return ORJSONResponse(res)


@object_router.post("/{object_name}")
async def create_object(
    object_name: str,
    data: dict,
    authorization: str = Header(),
    session: AsyncSession = Depends(get_session),
):
    object_class: AbstrackPesopolisObject = BaseFactory.get(object_name)
    res = await object_class.create(session, data)
    return ORJSONResponse(res)


@object_router.post("/{object_name}/many")
async def create_objects(
    object_name: str,
    data: List[dict],
    authorization: str = Header(),
    session: AsyncSession = Depends(get_session),
):
    object_class: AbstrackPesopolisObject = BaseFactory.get(object_name)
    res = await object_class.create_many(session, data)
    return ORJSONResponse(res)


@object_router.put("/{object_name}")
async def update_objects(
    object_name: str,
    data: List[dict],
    authorization: str = Header(),
    session: AsyncSession = Depends(get_session),
):
    object_class: AbstrackPesopolisObject = BaseFactory.get(object_name)
    res = await object_class.update_many(session, data)
    return ORJSONResponse(res)


@object_router.put("/{object_name}/{object_id}")
async def update_object(
    object_name: str,
    object_id: int,
    data: dict,
    authorization: str = Header(),
    session: AsyncSession = Depends(get_session),
):
    object_class: AbstrackPesopolisObject = BaseFactory.get(object_name)
    res = await object_class.update(session, object_id, data)
    return ORJSONResponse(res)


@object_router.delete("/{object_name}/{object_id}")
async def delete_object(
    object_name: str,
    object_id: int,
    authorization: str = Header(),
    session: AsyncSession = Depends(get_session),
):
    object_class: AbstrackPesopolisObject = BaseFactory.get(object_name)
    res = await object_class.delete(session, object_id)
    return ORJSONResponse(res)


@object_router.delete("/{object_name}")
async def delete_objects(
    object_name: str,
    object_ids: List[int],
    authorization: str = Header(),
    session: AsyncSession = Depends(get_session),
):
    object_class: AbstrackPesopolisObject = BaseFactory.get(object_name)
    res = await object_class.delete_many(session, object_ids)
    return ORJSONResponse(res)
