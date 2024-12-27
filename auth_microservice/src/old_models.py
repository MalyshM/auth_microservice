import re
from email_validator import EmailNotValidError, validate_email
from typing import AsyncGenerator, Optional, Self
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
    username: Optional[str] = Field(min_length=1, default=None)
    email: Optional[str] = Field(min_length=1, default=None)
    phone: Optional[str] = Field(min_length=11, max_length=12, default=None)

    @model_validator(mode="before")
    @classmethod
    def validate(cls, dict_values: dict) -> dict:
        if any(
            True
            for key, item in dict_values.items()
            if key in ["username", "email", "phone"] and item
        ):
            if "password" in dict_values:
                assert len(dict_values) == 2, (
                    "Exactly one of username, email or phone "
                    "must be provided and password"
                )
            else:
                assert (
                    len(dict_values) == 1
                ), "Exactly one of username, email or phone must be provided"
            return dict_values
        raise ValueError(
            "At least one of username, email or phone must be provided"
        )

    @model_validator(mode="after")
    def check_not_none(self) -> Self:
        if any(
            True for key in ["username", "email", "phone"] if getattr(self, key)
        ):
            return self
        raise ValueError(
            "At least one of username, email, or phone must not be None"
        )

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        try:
            validate_email(value, check_deliverability=False)
            return value
        except EmailNotValidError:
            return ""

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        match_obj = re.match(r".*?(8\d{10}|\+7\d{10}).*?", value)
        if match_obj:
            phone_str = match_obj.group(1)
            if len(phone_str) == 11 and phone_str[0] == "8":
                return phone_str
            if len(phone_str) == 12 and phone_str[0] == "+":
                return phone_str
        return ""

    @property
    def get_valid_field(self) -> tuple[str, str]:
        """Return a tuple of a valid field and its value.\n
        The first valid field in the order of username, email,
        phone is returned. If no fields are valid, returns
        empty tuple(only for type hinting).
        """
        for key in UserBase.model_fields.keys():
            if key in ["username", "email", "phone"] and getattr(
                self, key, None
            ):
                return key, getattr(self, key)
        return "", ""


class UserCreate(UserBase):
    password: str = Field(min_length=9)

    @field_validator("password")
    @classmethod
    def _validate(cls, value: str) -> str:
        # if len(value) < 9:
        #     raise ValueError(f"length should be at least {9}")

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
