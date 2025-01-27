from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from auth_microservice.src.connection import connect_db_data
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from auth_microservice.src.dynamic_models import (
    ID_FIELD,
    PASSWORD_FIELD,
    UserPublicDBType,
    UserCreateType,
    UserDBType,
)
from auth_microservice.src.routers.user_router import get_my_user
from auth_microservice.src.token_utils import (
    set_refresh_token_cookie,
)

reg_log_router = APIRouter(tags=["Registration/Login"])


@reg_log_router.post(
    "/register",
    response_model=UserPublicDBType,
)
async def register_user(
    request: Request,
    user: UserCreateType,
    session: AsyncSession = Depends(connect_db_data),
) -> UserPublicDBType:
    try:
        return await get_my_user(request, session)
    except HTTPException:
        pass
    try:
        async with session.begin():
            db_user = UserDBType(**user.model_dump())
            session.add(db_user)
    except IntegrityError as e:
        await session.rollback()
        try:
            return await login_user(request, user, session)
        except BaseException:
            pass
        raise HTTPException(
            status_code=400, detail=f"User  could not be registered. {e}"
        )
    return await login_user(request, user, session)


@reg_log_router.post(
    "/login",
    response_model=UserPublicDBType,
)
async def login_user(
    request: Request,
    user: UserCreateType,
    session: AsyncSession = Depends(connect_db_data),
) -> UserPublicDBType:
    try:
        return await get_my_user(request, session)
    except HTTPException:
        pass
    try:
        field, text = user.get_valid_field
        result = await session.execute(
            select(UserDBType).where(getattr(UserDBType, field) == text)
        )
        result = result.scalars().one()
        if getattr(result, PASSWORD_FIELD) != getattr(user, PASSWORD_FIELD):
            raise HTTPException(
                status_code=403, detail="User provided incorrect data."
            )
        rsp_body = UserPublicDBType(**result.model_dump())
    except IntegrityError as e:
        raise HTTPException(status_code=404, detail=f"User not found. {e}")
    except HTTPException as e:
        raise e
    except BaseException as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    model_dict = rsp_body.model_dump(exclude_none=True)
    model_dict[ID_FIELD] = str(model_dict[ID_FIELD])
    response = JSONResponse(content=model_dict, status_code=200)
    set_refresh_token_cookie(response, rsp_body)
    return response
