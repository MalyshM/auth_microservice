from typing import Sequence
from fastapi import Depends, FastAPI
from sqlmodel import select
from starlette.middleware.cors import CORSMiddleware

# from admin import UserAdmin, AdminAuth, ETLView
# from models import engine

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from sqlalchemy.ext.asyncio import AsyncSession

from auth_microservice.src.models import User, connect_db_data


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


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json", title="FastAPI API documentation"
    )


@app.get("/openapi.json", include_in_schema=False)
async def get_custom_openapi():
    return get_openapi(title="FastAPI", version="1.0", routes=app.routes)


@app.post("/user")
async def post_user(
    user: User, session: AsyncSession = Depends(connect_db_data)
) -> User:
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


#
@app.get("/user")
async def get_users(
    session: AsyncSession = Depends(connect_db_data),
) -> Sequence[User]:
    result = await session.execute(select(User))
    result = result.scalars().all()
    print(result)
    return result
