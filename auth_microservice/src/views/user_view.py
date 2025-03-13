from typing import Sequence
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from auth_microservice.src.crud.base_generic_crud import CRUD
from ..models.dynamic_db_models import UserDBType
from ..models.dynamic_models import (
    UserBase,
    UserCreateType,
    UserPublicDBType,
)


class UserCRUD(CRUD[UserPublicDBType, UserCreateType, UserDBType]):
    pass


class UserView:
    user_crud: UserCRUD = UserCRUD(
        UserPublicDBType, UserCreateType, UserDBType
    )

    @classmethod
    def create_rsp(cls, user: UserBase) -> dict:
        return user.model_dump(
            exclude_none=True, serialize_as_any=True, mode="json"
        )

    @classmethod
    def create_rsp_list(cls, user_list: Sequence[UserBase]) -> Sequence[dict]:
        return [UserView.create_rsp(user) for user in user_list]

    @classmethod
    async def create(
        cls,
        obj: UserCreateType,  # type: ignore # this is class, not var
        session: AsyncSession,
    ) -> dict:
        user = await UserView.user_crud.create(obj, session)
        return UserView.create_rsp(user)

    @classmethod
    async def read(cls, id: UUID, session: AsyncSession) -> dict:
        user = await UserView.user_crud.read(id, session)
        return UserView.create_rsp(user)

    @classmethod
    async def read_all(cls, session: AsyncSession) -> Sequence[dict]:
        user = await UserView.user_crud.read_all(session)
        return UserView.create_rsp_list(user)

    @classmethod
    async def update(
        cls,
        obj: UserPublicDBType,  # type: ignore # this is class, not var
        session: AsyncSession,
    ) -> dict:
        user = await UserView.user_crud.update(obj, session)
        return UserView.create_rsp(user)

    @classmethod
    async def delete(cls, id: UUID, session: AsyncSession) -> dict:
        user = await UserView.user_crud.delete(id, session)
        return UserView.create_rsp(user)
