import time
from typing import Sequence
from fastapi import Depends, FastAPI, HTTPException, Request
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

from auth_microservice.src.dynamic_models import (
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
async def log_requests(request: Request, call_next):
    base_logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    base_logger.info(f"Response: {response.status_code}")
    return response


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


#
@app.get("/user", response_model=Sequence[UserBaseType])
async def get_users(
    session: AsyncSession = Depends(connect_db_data),
) -> Sequence[UserBaseType]:
    result = await session.execute(select(UserType))
    return result.scalars().all()
