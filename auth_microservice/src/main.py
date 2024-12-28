import time
from typing import Sequence
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlmodel import select
from starlette.middleware.cors import CORSMiddleware

# from admin import UserAdmin, AdminAuth, ETLView
# from models import engine
from sqlalchemy.exc import IntegrityError
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from sqlalchemy.ext.asyncio import AsyncSession
from auth_microservice.src.connection import connect_db_data
from auth_microservice.src.logger import base_logger
from starlette.middleware.base import _StreamingResponse
from auth_microservice.src.dynamic_models import (
    PASSWORD_FIELD,
    UserBaseType,
    UserType,
    UserPublicType,
    UserCreateType,
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
    # application.include_router(main_page_router)
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
    response_body = b"".join(
        [chunk async for chunk in response.body_iterator]  # type: ignore
    )
    if 200 <= response.status_code <= 399:
        base_logger.info(f"Info about requst:\n{log_string}")
    else:
        log_string += f"Response result: {response_body.decode()}\n"
        base_logger.error(f"Info about request:\n{log_string}")
    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=response.headers,
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
    start = time.monotonic()
    try:
        async with session.begin():
            db_user = UserType(**user.model_dump())
            session.add(db_user)
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=400, detail=f"User  could not be created. {e}"
        )
    base_logger.info(f"route post_user /user Time: {time.monotonic() - start}")
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
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
async def register_user(
    user: UserCreateType,
    session: AsyncSession = Depends(connect_db_data),
) -> UserPublicType:
    start = time.monotonic()
    try:
        async with session.begin():
            db_user = UserType(**user.model_dump())
            session.add(db_user)
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=400, detail=f"User  could not be registered. {e}"
        )
    base_logger.info(f"route post_user /user Time: {time.monotonic() - start}")
    return UserPublicType(**db_user.model_dump())
