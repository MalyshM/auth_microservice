from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..connection import connect_db_data
from ..docs.responses import (
    logout_200,
    reg_response_400,
    response_400_general,
    response_401,
    response_403,
    response_404,
)
from ..logger import base_logger
from ..models.dynamic_db_models import UserDBType
from ..models.dynamic_models import (
    ID_FIELD,
    PASSWORD_FIELD,
    UserCreateType,
    UserPublicDBType,
)
from ..routers.user_router import get_my_user
from ..token_utils import delete_cookie_tokens, set_cookie_tokens

reg_log_router = APIRouter(tags=["Registration/Login"])


@reg_log_router.post(
    "/register",
    summary="Register a New User",
    description=(
        "Registers a new user by creating a new user account. "
        "If the user already exists, it attempts to log in the user instead."
    ),
    response_model=Sequence[UserPublicDBType],
    responses={
        401: response_401,
        400: reg_response_400,
    },
)
async def register_user(
    request: Request,
    user: UserCreateType,  # type: ignore # this is class, not var
    session: AsyncSession = Depends(connect_db_data),
) -> JSONResponse:  # type: ignore # this is class, not var
    try:
        return await get_my_user(request, session)
    except HTTPException:
        pass
    try:
        async with session.begin():
            db_user = UserDBType(**user.model_dump())
            session.add(db_user)
    except IntegrityError as e:
        try:
            return await login_user(request, user, session)
        except BaseException:
            pass
        base_logger.error(e)
        raise HTTPException(
            status_code=400, detail="User could not be registered."
        )
    return await login_user(request, user, session)


@reg_log_router.post(
    "/login",
    summary="Log In a User",
    description=(
        "Logs in a user by verifying their credentials. "
        "If successful, returns the user's public information."
    ),
    response_model=Sequence[UserPublicDBType],
    responses={
        401: response_401,
        400: response_400_general,
        403: response_403,
        404: response_404,
    },
)
async def login_user(
    request: Request,
    user: UserCreateType,  # type: ignore # this is class, not var
    session: AsyncSession = Depends(connect_db_data),
) -> JSONResponse:  # type: ignore # this is class, not var
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
        base_logger.error(e)
        raise HTTPException(status_code=404, detail="User not found.")
    except NoResultFound as e:
        base_logger.error(e)
        raise HTTPException(status_code=404, detail="User not found.")
    except HTTPException as e:
        base_logger.error(e)
        raise e
    except BaseException as e:
        base_logger.error(e)
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    model_dict = rsp_body.model_dump(exclude_none=True)
    model_dict[ID_FIELD] = str(model_dict[ID_FIELD])
    response = JSONResponse(content=model_dict, status_code=200)
    set_cookie_tokens(response, rsp_body)
    return response


@reg_log_router.post(
    "/logout",
    summary="Log Out a User",
    description="Logs out a user by clearing their authentication cookies.",
    responses={200: logout_200},
)
async def logout_user() -> JSONResponse:
    resp = JSONResponse(
        content={"detail": "Successfully logged out."}, status_code=200
    )
    delete_cookie_tokens(resp)
    return resp
