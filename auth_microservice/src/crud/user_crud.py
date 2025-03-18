from typing import Sequence

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..models.dynamic_db_models import UserDBType
from ..models.dynamic_models import UserBase, UserCreateType, UserPublicDBType
from .base_generic_crud import CRUD


class UserCRUD(CRUD[UserPublicDBType, UserCreateType, UserDBType]):
    name = "User"

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
            self.logger.error(e)
            raise HTTPException(
                status_code=404, detail=f"{self.name} not found."
            )
        rsp_list = []
        for item in result:
            rsp_list.append(
                self.entity(
                    **item.model_dump(exclude_none=True, serialize_as_any=True)
                )
            )
        return rsp_list
