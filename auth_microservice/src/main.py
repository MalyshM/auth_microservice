import time
from typing import Sequence
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from sqlmodel import select
from starlette.middleware.cors import CORSMiddleware


from sqlalchemy.exc import IntegrityError
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from sqlalchemy.ext.asyncio import AsyncSession
from auth_microservice.src.connection import connect_db_data
from auth_microservice.src.logger import base_logger
from starlette.middleware.base import _StreamingResponse
from auth_microservice.src.dynamic_models import (
    ID_FIELD,
    PASSWORD_FIELD,
    UserBaseType,
    UserType,
    UserPublicType,
    UserCreateType,
)
from auth_microservice.src.token_utils import (
    create_access_token,
    create_refresh_token,
    set_cookie_tokens,
)


def get_application() -> FastAPI:
    application = FastAPI(root_path="/auth")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


app = get_application()


@app.middleware("http")
async def log_requests(request: Request, call_next) -> Response:
    log_string = ""
    client_ip = f"user_ip: {request.client.host}" if request.client else ""
    log_string += f"Request: {request.method} {request.url}, {client_ip}\n"
    body = await request.body()
    if body:
        log_string += f"Request Body: \n{body.decode()}\n"
    query_params = request.query_params
    if query_params:
        log_string += f"Query Parameters: {query_params}\n"
    start = time.monotonic()
    response: _StreamingResponse = await call_next(request)
    log_string += f"Response Status Code: {response.status_code}\n"
    elapsed_time = time.monotonic() - start
    log_string += f"Request Time: {elapsed_time:.4f} seconds\n"
    response_body = b"".join([chunk async for chunk in response.body_iterator])
    response.headers["Content-Length"] = str(len(response_body))
    if 200 <= response.status_code <= 399:
        log_string += f"Response result: {response_body.decode()}\n"
        base_logger.info(f"Info about request:\n{log_string}")
    else:
        log_string += f"Response result: {response_body.decode()}\n"
        base_logger.error(f"Info about request:\n{log_string}")
    return Response(
        content=response_body,
        status_code=response.status_code,
        media_type=response.media_type,
        headers=dict(response.headers),
    )


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json", title="FastAPI API documentation"
    )


@app.get("/openapi.json", include_in_schema=False)
async def get_custom_openapi():
    return get_openapi(title="FastAPI", version="1.0", routes=app.routes)


@app.post("/user", response_model=UserPublicType)
async def post_user(
    user: UserCreateType,
    session: AsyncSession = Depends(connect_db_data),
) -> UserPublicType:
    try:
        async with session.begin():
            db_user = UserType(**user.model_dump())
            session.add(db_user)
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=400, detail=f"User  could not be created. {e}"
        )
    return UserPublicType(**db_user.model_dump())


@app.get(
    "/user",
    response_model=Sequence[UserBaseType],
)
async def get_users(
    session: AsyncSession = Depends(connect_db_data),
) -> Sequence[UserBaseType]:
    result = await session.execute(select(UserType))
    return result.scalars().all()


@app.post(
    "/register",
    response_model=UserPublicType,
)
async def register_user(
    user: UserCreateType,
    session: AsyncSession = Depends(connect_db_data),
) -> UserPublicType:
    try:
        async with session.begin():
            db_user = UserType(**user.model_dump())
            session.add(db_user)
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=400, detail=f"User  could not be registered. {e}"
        )
    return await login_user(user, session)


@app.post(
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
            select(UserType).where(getattr(UserType, field) == text)
        )
        result = result.scalars().one()
        if getattr(result, PASSWORD_FIELD) != getattr(user, PASSWORD_FIELD):
            raise HTTPException(
                status_code=403, detail="User provided incorrect data."
            )
        rsp_body = UserPublicType(**result.model_dump())
    except IntegrityError as e:
        raise HTTPException(status_code=404, detail=f"User not found. {e}")
    except HTTPException as e:
        raise e
    except BaseException as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    model_dict = rsp_body.model_dump(exclude_none=True)
    model_dict[ID_FIELD] = str(model_dict[ID_FIELD])
    response = JSONResponse(content=model_dict, status_code=200)
    set_cookie_tokens(response, rsp_body)
    return response
