# TODO модели и схемы должны быть одним и тем же и сделаны через sqlmodel
# TODO https://github.com/fastapi/sqlmodel
from typing import AsyncGenerator, Optional
import uuid
from pydantic import field_validator, model_validator
from sqlmodel import Field, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost/auth_users"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_vkr = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
#  -> AsyncGenerator[AsyncSession]


async def connect_db_data() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_vkr() as session:
        yield session


class UserBase(SQLModel):
    username: Optional[str]
    email: Optional[str]
    phone: Optional[str]

    @model_validator(mode="before")
    @classmethod
    def validate(cls, dict_values: dict) -> dict:
        if any(
            True
            for key, item in dict_values.items()
            if key in ["username", "email", "phone"] and item
        ):
            return dict_values
        raise ValueError(
            "At least one of username, email or phone must be provided"
        )


class UserCreate(UserBase):
    password: str = Field(min_length=9)

    @field_validator("password", mode="after")
    @classmethod
    def _validate(cls, value: str) -> str:
        if len(value) < 9:
            raise ValueError(f"length should be at least {9}")

        if not any(char.isdigit() for char in value):
            raise ValueError("Password should have at least one numeral")

        if not any(char.isupper() for char in value):
            raise ValueError(
                "Password should have at least one uppercase letter"
            )

        if not any(char.islower() for char in value):
            raise ValueError(
                "Password should have at least one lowercase letter"
            )
        return value


class UserPublic(UserBase):
    id: uuid.UUID


class User(UserCreate, table=True):
    __tablename__: str = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
