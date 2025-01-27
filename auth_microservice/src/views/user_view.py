from typing import Sequence
from sqlmodel import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from auth_microservice.src.models.dynamic_models import (
    ID_FIELD,
    UserBase,
    UserBaseType,
    UserPublicType,
    UserPublicDBType,
    UserCreateType,
)
from auth_microservice.src.models.dynamic_db_models import UserDBType

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


class UserView:
    @classmethod
    async def form_rsp_list(cls, result: Sequence[UserBase]) -> Sequence:
        rsp_list = []
        for item in result:
            rsp_list.append(
                UserPublicDBType(
                    **item.model_dump(exclude_none=True, serialize_as_any=True)
                ).model_dump(
                    exclude_none=True, serialize_as_any=True, mode="json"
                )
            )
        return rsp_list

    @classmethod
    async def create_user(
        cls, user: UserCreateType, session: AsyncSession
    ) -> UserPublicType:
        try:
            async with session.begin():
                db_user = UserDBType(**user.model_dump())
                session.add(db_user)
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=400, detail=f"User  could not be created. {e}"
            )
        return UserPublicDBType(**db_user.model_dump(exclude_none=True))

    @classmethod
    async def update_user(
        cls, user: UserPublicDBType, session: AsyncSession
    ) -> UserPublicType:
        try:
            async with session.begin():
                await session.execute(
                    update(UserDBType)
                    .where(getattr(UserDBType, ID_FIELD) == user.id)
                    .values(**user.model_dump(exclude_none=True))
                )
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=400, detail=f"User  could not be created. {e}"
            )
        return UserPublicDBType(**user.model_dump(exclude_none=True))

    @classmethod
    async def get_user(cls, user_id: str, session: AsyncSession) -> Sequence:
        result = await session.execute(
            select(UserDBType).where(getattr(UserDBType, ID_FIELD) == user_id)
        )
        result = result.scalars().all()
        return await UserView.form_rsp_list(result)

    @classmethod
    async def delete_user(
        cls, user_id: str, session: AsyncSession
    ) -> list[dict]:
        try:
            async with session.begin():
                await session.execute(
                    delete(UserDBType).where(
                        getattr(UserDBType, ID_FIELD) == user_id
                    )
                )
            return [{"status": "success"}]
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=400, detail=f"User  could not be deleted. {e}"
            )

    @classmethod
    async def get_users_by_field(
        cls, user: UserBaseType, session: AsyncSession
    ) -> Sequence:
        field, text = user.get_valid_field
        result = await session.execute(
            select(UserDBType).where(
                getattr(UserDBType, field).ilike(f"%{text}%")
            )
        )
        result = result.scalars().all()
        return await UserView.form_rsp_list(result)

    @classmethod
    async def get_users(cls, session: AsyncSession) -> Sequence:
        result = await session.execute(select(UserDBType))
        result = result.scalars().all()
        return await UserView.form_rsp_list(result)
