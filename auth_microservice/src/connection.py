import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

load_dotenv()

DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv("DB_USER", "")}:"
    f"{os.getenv("DB_PASSWORD", "")}@{os.getenv("DB_HOST", "")}:"
    f"{os.getenv('DB_PORT', '5432')}/{os.getenv("DB_NAME", "")}"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    echo_pool=True,
    pool_size=20,
    pool_pre_ping=True,
    max_overflow=5,
)
async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=True
)


async def connect_db_data() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
