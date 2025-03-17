from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from .base_generic_crud import CRUD
from ..models.dynamic_db_models import UserDBType
from ..models.dynamic_models import (
    UserBase,
    UserCreateType,
    UserPublicDBType,
)


class UserCRUD(CRUD[UserPublicDBType, UserCreateType, UserDBType]):

    async def get_users_by_field(
        self, user: UserBase, session: AsyncSession
    ) -> Sequence[UserBase]:
        field, text = user.get_valid_field
        try:
            result = await session.execute(
                select(self.db_entity).where(
                    getattr(self.db_entity, field).ilike(f"%{text}%")
                )
            )
            result = result.scalars().all()
        except NoResultFound as e:
            raise HTTPException(status_code=404, detail=f"User not found. {e}")
        rsp_list = []
        for item in result:
            rsp_list.append(
                self.entity(
                    **item.model_dump(exclude_none=True, serialize_as_any=True)
                )
            )
        return rsp_list
