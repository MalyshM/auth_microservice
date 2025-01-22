from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from auth_microservice.src.connection import connect_db_data
from auth_microservice.src.dynamic_models import (
    UserBaseType,
    UserPublicType,
    UserPublicDBType,
    UserCreateType,
)
from auth_microservice.src.views.user_view import UserView

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post(
    "", response_model=UserPublicDBType, response_model_exclude_none=True
)
async def post_user(
    user: UserCreateType,
    session: AsyncSession = Depends(connect_db_data),
) -> UserPublicDBType:
    try:
        return await UserView.create_user(user, session)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"User  could not be created. {e}"
        )


@user_router.get(
    "",
    response_model=Sequence[UserPublicDBType],
    response_model_exclude_none=True,
)
async def get_users(
    session: AsyncSession = Depends(connect_db_data),
) -> Sequence:
    return await UserView.get_users(session)


@user_router.get(
    "/{user_id}",
    response_model=Sequence[UserPublicDBType],
    response_model_exclude_none=True,
)
async def get_user(
    user_id: str,
    session: AsyncSession = Depends(connect_db_data),
) -> Sequence:
    return await UserView.get_user(user_id, session)


@user_router.post(
    "/user_by_field",
    response_model=Sequence[UserPublicDBType],
    response_model_exclude_none=True,
)
async def get_users_by_field(
    user: UserBaseType,
    session: AsyncSession = Depends(connect_db_data),
) -> Sequence:
    return await UserView.get_users_by_field(user, session)


@user_router.put(
    "/{user_id}",
    response_model=UserPublicDBType,
    response_model_exclude_none=True,
)
async def update_user(
    user: UserPublicDBType,
    session: AsyncSession = Depends(connect_db_data),
) -> UserPublicType:
    return await UserView.update_user(user, session)


@user_router.delete(
    "/user/{user_id}",
)
async def delete_user(
    user_id: str,
    session: AsyncSession = Depends(connect_db_data),
) -> dict:
    return await UserView.delete_user(user_id, session)
