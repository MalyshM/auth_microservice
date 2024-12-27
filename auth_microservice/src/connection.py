from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost/auth_users"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_vkr = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def connect_db_data() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_vkr() as session:
        yield session
