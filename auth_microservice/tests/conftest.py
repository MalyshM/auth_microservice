from fastapi.testclient import TestClient
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)
from typing import AsyncGenerator

from auth_microservice.src.models.dynamic_db_models import UserDBType

from auth_microservice.src.connection import connect_db_data
from auth_microservice.src.main import app


@pytest_asyncio.fixture
def client():
    return TestClient(app)


@pytest_asyncio.fixture()
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    global IS_CREATED_META
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with engine.begin() as conn:
        await conn.run_sync(UserDBType.metadata.create_all)
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
def override_db_dependency(async_session):
    app.dependency_overrides[connect_db_data] = lambda: async_session
    yield
    app.dependency_overrides.clear()
