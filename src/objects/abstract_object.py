from abc import ABC, abstractmethod
from typing import Any, Dict, List

from pydantic import BaseModel
from sqlalchemy import delete, insert, select
from sqlalchemy import update as _update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import AbstractTable
from exceptions import PesopolistException


class AbstrackPesopolisObject(ABC):
    _table_class: AbstractTable
    _model_class: BaseModel

    @classmethod
    @abstractmethod
    async def create(
        cls,
        session: AsyncSession,
        data: Dict[str, Any],
        from_other_object: bool = False,
    ) -> Dict[str, int]:
        model_data = cls._model_class.model_validate(data)
        del data

        created_id = (
            await session.execute(
                insert(cls._table_class)
                .values(model_data.model_dump())
                .returning(cls._table_class.id)
            )
        ).scalar()

        if not from_other_object:
            await session.commit()

        return {"created_id": created_id}

    @classmethod
    @abstractmethod
    async def create_many(
        cls,
        session: AsyncSession,
        data: List[Dict[str, Any]],
        from_other_object: bool = False,
    ) -> Dict[str, List[int]]:
        created_ids = []
        for elem in data:
            created_ids.append((await cls.create(session, elem, True))["created_id"])

        if not from_other_object:
            await session.commit()

        return {"created_ids": created_ids}

    @classmethod
    @abstractmethod
    async def get(
        cls, session: AsyncSession, data: Dict[str, Any] | None
    ) -> List[Dict[str, Any]]:
        pass

    @classmethod
    async def get_one(
        cls, session: AsyncSession, object_id: int, data: Dict[str, Any] | None
    ) -> Dict[str, Any]:
        answer = (
            await session.execute(
                select(cls._table_class).where(cls._table_class.id == object_id)
            )
        ).scalar()

        if not answer:
            raise PesopolistException("Object not found", 404)

        return answer.as_dict()

    @classmethod
    @abstractmethod
    async def update(
        cls,
        session: AsyncSession,
        object_id: int,
        data: Dict[str, Any],
        from_other_object: bool = False,
    ) -> Dict[str, Any]:
        await session.execute(
            _update(cls._table_class)
            .values(**data)
            .where(cls._table_class.id == object_id)
        )

        if not from_other_object:
            await session.commit()

        return {"updated_id": object_id}

    @classmethod
    @abstractmethod
    async def update_many(
        cls,
        session: AsyncSession,
        data: List[Dict[str, Any]],
        from_other_object: bool = False,
    ) -> Dict[str, List[int]]:
        updated_ids = []
        for elem in data:
            updated_ids.append(
                (await cls.update(session, elem.pop("id"), elem, True))["updated_id"]
            )

        if not from_other_object:
            await session.commit()

        return {"updated_ids": updated_ids}

    @classmethod
    @abstractmethod
    async def delete(
        cls, session: AsyncSession, object_id: int, from_other_object: bool = False
    ) -> Dict[str, Any]:
        await session.execute(
            delete(cls._table_class).where(cls._table_class.id == object_id)
        )

        if not from_other_object:
            await session.commit()

        return {"deleted_id": object_id}

    @classmethod
    @abstractmethod
    async def delete_many(
        cls,
        session: AsyncSession,
        object_ids: List[int],
        from_other_object: bool = False,
    ) -> Dict[str, List[int]]:
        updated_ids = []
        for elem_id in object_ids:
            updated_ids.append((await cls.delete(session, elem_id, True))["deleted_id"])

        if not from_other_object:
            await session.commit()

        return {"deleted_ids": updated_ids}
