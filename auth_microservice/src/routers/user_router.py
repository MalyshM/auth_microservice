from typing import Optional, Sequence
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from auth_microservice.src.connection import connect_db_data
from auth_microservice.src.dynamic_models import (
    ID_FIELD,
    UserBaseType,
    UserPublicDBType,
    UserCreateType,
)
from auth_microservice.src.routers.auth_router import auth
from auth_microservice.src.token_utils import (
    refresh_access_token,
    verify_refresh_token,
)
from auth_microservice.src.views.user_view import UserView
from auth_microservice.src.logger import base_logger


async def auth_dependency(request: Request) -> Optional[str]:
    base_logger.info("Auth dependency")
    try:
        json_resp = await auth(request)
        return json_resp.headers.get("Set-Cookie")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error: {e}")


def make_resp(
    res: Sequence, request: Request, set_cookie: Optional[str] = None
):
    response = JSONResponse(content=res, status_code=200)
    if set_cookie:
        refresh_access_token(response, request.cookies["refresh_token"])
    return response


user_router = APIRouter(
    prefix="/user", tags=["User"], dependencies=[Depends(auth_dependency)]
)


@user_router.post(
    "", response_model=UserPublicDBType, response_model_exclude_none=True
)
async def post_user(
    request: Request,
    user: UserCreateType,
    session: AsyncSession = Depends(connect_db_data),
    set_cookie: Optional[str] = Depends(auth_dependency),
) -> JSONResponse:
    res = await UserView.create_user(user, session)
    return make_resp(res, request, set_cookie)


@user_router.get(
    "",
    response_model=Sequence[UserPublicDBType],
    response_model_exclude_none=True,
)
async def get_users(
    request: Request,
    session: AsyncSession = Depends(connect_db_data),
    set_cookie: Optional[str] = Depends(auth_dependency),
) -> JSONResponse:
    res = await UserView.get_users(session)
    return make_resp(res, request, set_cookie)


@user_router.get(
    "/me",
    response_model=Sequence[UserPublicDBType],
    response_model_exclude_none=True,
)
async def get_my_user(
    request: Request,
    session: AsyncSession = Depends(connect_db_data),
    set_cookie: Optional[str] = Depends(auth_dependency),
) -> JSONResponse:
    payload = verify_refresh_token(request.cookies["refresh_token"])
    if not payload:
        raise HTTPException(status_code=401, detail="Not authenticated")
    res = await UserView.get_user(str(payload[ID_FIELD]), session)
    return make_resp(res, request, set_cookie)


@user_router.get(
    "/{user_id}",
    response_model=Sequence[UserPublicDBType],
    response_model_exclude_none=True,
)
async def get_user(
    request: Request,
    user_id: str,
    session: AsyncSession = Depends(connect_db_data),
    set_cookie: Optional[str] = Depends(auth_dependency),
) -> JSONResponse:
    res = await UserView.get_user(user_id, session)
    return make_resp(res, request, set_cookie)


@user_router.post(
    "/user_by_field",
    response_model=Sequence[UserPublicDBType],
    response_model_exclude_none=True,
)
async def get_users_by_field(
    request: Request,
    user: UserBaseType,
    session: AsyncSession = Depends(connect_db_data),
    set_cookie: Optional[str] = Depends(auth_dependency),
) -> JSONResponse:
    res = await UserView.get_users_by_field(user, session)
    return make_resp(res, request, set_cookie)


@user_router.put(
    "/{user_id}",
    response_model=UserPublicDBType,
    response_model_exclude_none=True,
)
async def update_user(
    request: Request,
    user: UserPublicDBType,
    session: AsyncSession = Depends(connect_db_data),
    set_cookie: Optional[str] = Depends(auth_dependency),
) -> JSONResponse:
    res = await UserView.update_user(user, session)
    return make_resp(res, request, set_cookie)


@user_router.delete(
    "/user/{user_id}",
)
async def delete_user(
    request: Request,
    user_id: str,
    session: AsyncSession = Depends(connect_db_data),
    set_cookie: Optional[str] = Depends(auth_dependency),
) -> JSONResponse:
    res = await UserView.delete_user(user_id, session)
    return make_resp(res, request, set_cookie)
