from typing import Optional, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..connection import connect_db_data
from ..dependencies.auth_dependency import auth_dependency
from ..docs.responses import (
    create_response_400,
    delete_response_400,
    response_401,
    response_404,
    update_response_400,
)
from ..models.dynamic_models import (
    ID_FIELD,
    UserBaseType,
    UserCreateType,
    UserPublicDBType,
)
from ..token_utils import refresh_access_token, verify_refresh_token
from ..views.user_view import UserView


def make_resp(
    res: Sequence, request: Request, set_cookie: Optional[str] = None
):
    response = JSONResponse(content=res, status_code=200)
    if set_cookie:
        refresh_access_token(response, request.cookies["refresh_token"])
    return response


user_router = APIRouter(
    prefix="/user",
    tags=["User"],
    dependencies=[Depends(auth_dependency)],
    responses={401: response_401},
)


@user_router.post(
    "",
    summary="Create a New User",
    description="Creates a new user in the system.",
    response_model=Sequence[UserPublicDBType],
    response_model_exclude_none=True,
    responses={
        400: create_response_400,
    },
)
async def post_user(
    request: Request,
    user: UserCreateType,  # type: ignore # this is class, not var
    session: AsyncSession = Depends(connect_db_data),
    set_cookie: Optional[str] = Depends(auth_dependency),
) -> JSONResponse:
    res = await UserView.create_user(user, session)
    return make_resp(res, request, set_cookie)


@user_router.get(
    "",
    summary="Get All Users",
    description="Retrieves a list of all users in the system.",
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
    summary="Get Current User",
    description="Retrieves the currently authenticated user's information.",
    response_model=Sequence[UserPublicDBType],
    response_model_exclude_none=True,
    responses={
        404: response_404,
    },
)
async def get_my_user(
    request: Request,
    session: AsyncSession = Depends(connect_db_data),
    set_cookie: Optional[str] = Depends(auth_dependency),
) -> JSONResponse:
    if not request.cookies.get("refresh_token"):
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = verify_refresh_token(request.cookies["refresh_token"])
    if not payload:
        raise HTTPException(status_code=401, detail="Not authenticated")
    res = await UserView.get_user(UUID(payload[ID_FIELD]), session)
    return make_resp(res, request, set_cookie)


@user_router.get(
    "/{user_id}",
    summary="Get User by ID",
    description="Retrieves a user by their unique ID.",
    response_model=Sequence[UserPublicDBType],
    response_model_exclude_none=True,
    responses={
        404: response_404,
    },
)
async def get_user(
    request: Request,
    user_id: str,
    session: AsyncSession = Depends(connect_db_data),
    set_cookie: Optional[str] = Depends(auth_dependency),
) -> JSONResponse:
    res = await UserView.get_user(UUID(user_id), session)
    return make_resp(res, request, set_cookie)


@user_router.post(
    "/user_by_field",
    summary="Get Users by Field",
    description="Retrieves users based on a specific field.",
    response_model=Sequence[UserPublicDBType],
    response_model_exclude_none=True,
)
async def get_users_by_field(
    request: Request,
    user: UserBaseType,  # type: ignore # this is class, not var
    session: AsyncSession = Depends(connect_db_data),
    set_cookie: Optional[str] = Depends(auth_dependency),
) -> JSONResponse:
    res = await UserView.get_users_by_field(user, session)
    return make_resp(res, request, set_cookie)


@user_router.put(
    "/{user_id}",
    summary="Update User",
    description="Updates the information of an existing user.",
    response_model=Sequence[UserPublicDBType],
    response_model_exclude_none=True,
    responses={
        400: update_response_400,
    },
)
async def update_user(
    request: Request,
    user: UserPublicDBType,  # type: ignore # this is class, not var
    session: AsyncSession = Depends(connect_db_data),
    set_cookie: Optional[str] = Depends(auth_dependency),
) -> JSONResponse:
    res = await UserView.update_user(user, session)
    return make_resp(res, request, set_cookie)


@user_router.delete(
    "/user/{user_id}",
    summary="Delete User",
    description="Deletes a user from the system by their unique ID.",
    responses={
        400: delete_response_400,
    },
)
async def delete_user(
    request: Request,
    user_id: str,
    session: AsyncSession = Depends(connect_db_data),
    set_cookie: Optional[str] = Depends(auth_dependency),
) -> JSONResponse:
    res = await UserView.delete_user(UUID(user_id), session)
    return make_resp(res, request, set_cookie)
