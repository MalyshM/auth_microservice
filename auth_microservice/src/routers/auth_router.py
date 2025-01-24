from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from auth_microservice.src.connection import connect_db_data
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from auth_microservice.src.dynamic_models import (
    ID_FIELD,
    PASSWORD_FIELD,
    UserPublicType,
    UserPublicDBType,
    UserCreateType,
    UserDBType,
)
from auth_microservice.src.token_utils import (
    refresh_access_token,
    set_refresh_token_cookie,
    verify_access_token,
    verify_refresh_token,
)

auth_router = APIRouter(tags=["Auth"])


@auth_router.post(
    "/register",
    response_model=UserPublicType,
)
async def register_user(
    user: UserCreateType,
    session: AsyncSession = Depends(connect_db_data),
) -> UserPublicType:
    try:
        async with session.begin():
            db_user = UserDBType(**user.model_dump())
            session.add(db_user)
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=400, detail=f"User  could not be registered. {e}"
        )
    return await login_user(user, session)


@auth_router.post(
    "/login",
    response_model=UserPublicType,
)
async def login_user(
    user: UserCreateType,
    session: AsyncSession = Depends(connect_db_data),
) -> UserPublicType:
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


@auth_router.get(
    "/auth",
)
async def auth(
    request: Request,
) -> Response:
    cookies = request.cookies
    payload = (
        verify_access_token(cookies["access_token"])
        if cookies.get("access_token")
        else None
    )
    if not payload:
        try:
            refresh_token = (
                cookies["refresh_token"]
                if cookies.get("refresh_token")
                else None
            )
            if not refresh_token:
                raise HTTPException(status_code=401, detail="Not authenticated")
            payload = verify_refresh_token(refresh_token)
            if not payload:
                raise HTTPException(status_code=401, detail="Not authenticated")
            response = JSONResponse(content=payload[ID_FIELD], status_code=200)
            refresh_access_token(response, cookies["refresh_token"])
            return response
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Error: {e}")
    else:
        return JSONResponse(content=payload[ID_FIELD], status_code=200)
