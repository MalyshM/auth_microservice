from typing import AsyncGenerator

import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from src.connection import connect_db_data
from src.main import app
from src.models.dynamic_db_models import UserDBType


@pytest_asyncio.fixture
def client():
    return TestClient(app)


@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(UserDBType.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
def async_session_factory(engine):
    return async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )


@pytest_asyncio.fixture
async def async_session(
    async_session_factory,
) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


@pytest_asyncio.fixture
def override_db_dependency(async_session_factory):
    async def get_session() -> AsyncGenerator[AsyncSession, None]:
        async with async_session_factory() as session:
            yield session

    app.dependency_overrides[connect_db_data] = get_session
    yield
    app.dependency_overrides.clear()
