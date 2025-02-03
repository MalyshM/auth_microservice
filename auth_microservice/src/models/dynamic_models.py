import copy
import os
import re
import uuid
from typing import Optional

from dotenv import load_dotenv
from email_validator import EmailNotValidError, validate_email
from pydantic import create_model, field_validator, model_validator
from sqlmodel import Field, SQLModel

from ..password_utils import hash_password

load_dotenv()
USERNAME_FIELD = os.getenv("USERNAME_FIELD", "")
EMAIL_FIELD = os.getenv("EMAIL_FIELD", "")
PHONE_FIELD = os.getenv("PHONE_FIELD", "")
PASSWORD_FIELD = os.getenv("PASSWORD_FIELD", "")
ID_FIELD = os.getenv("ID_FIELD", "")
TABLE_NAME = os.getenv("TABLE_NAME", "")


def validate(cls, dict_values: dict) -> dict:
    if any(
        True
        for key, item in dict_values.items()
        if key in [USERNAME_FIELD, EMAIL_FIELD, PHONE_FIELD] and item
    ):
        copy_dict = copy.deepcopy(dict_values)
        for k, v in copy_dict.items():
            if not v or k not in cls.model_json_schema()["properties"].keys():
                del dict_values[k]
        if PASSWORD_FIELD in dict_values:
            if ID_FIELD in dict_values:
                assert len(dict_values) == 3, (
                    "Exactly one of username, email or phone "
                    "must be provided and password and id"
                )
            else:
                assert len(dict_values) == 2, (
                    "Exactly one of username, email or phone "
                    "must be provided and password"
                )
        else:
            if ID_FIELD in dict_values:
                assert len(dict_values) == 2, (
                    "Exactly one of username, email or phone "
                    "must be provided and id"
                )
            else:
                assert (
                    len(dict_values) == 1
                ), "Exactly one of username, email or phone must be provided"
        return dict_values
    raise ValueError(
        "At least one of username, email or phone must be provided"
    )


def check_not_none(self):
    if any(
        True
        for key in [USERNAME_FIELD, EMAIL_FIELD, PHONE_FIELD]
        if getattr(self, key)
    ):
        return self
    raise ValueError(
        "check_not_none func At least one of username, "
        "email, or phone must not be None"
    )


def validate_email_(cls, value: str) -> str:
    try:
        validate_email(value, check_deliverability=False)
        return value
    except EmailNotValidError:
        return ""


def validate_phone(cls, value: str) -> str:
    match_obj = re.match(r".*?(8\d{10}|\+7\d{10}).*?", value)
    if match_obj:
        phone_str = match_obj.group(1)
        if len(phone_str) == 11 and phone_str[0] == "8":
            return phone_str
        if len(phone_str) == 12 and phone_str[0] == "+":
            return phone_str
    return ""


validators = {}
validators["validate"] = model_validator(mode="before")(validate)
validators["check_not_none"] = model_validator(mode="after")(check_not_none)

field_definitions = {}
if USERNAME_FIELD:
    field_definitions[USERNAME_FIELD] = (
        Optional[str],
        Field(
            min_length=1,
            default=None,
            unique=True,
            title="Username",
            description=(
                "The username of the user. Must "
                "be at least 1 character long and unique."
            ),
        ),
    )


if EMAIL_FIELD:
    field_definitions[EMAIL_FIELD] = (
        Optional[str],
        Field(
            min_length=1,
            default=None,
            unique=True,
            title="Email",
            description=(
                "The email address of the user. Must "
                "be a valid email format and unique."
            ),
        ),
    )
    validators["validate_email_"] = field_validator(EMAIL_FIELD)(
        validate_email_
    )

if PHONE_FIELD:
    field_definitions[PHONE_FIELD] = (
        Optional[str],
        Field(
            min_length=11,
            max_length=12,
            default=None,
            unique=True,
            title="Phone Number",
            description=(
                "The phone number of the user. Must "
                "be between 11 and 12 characters long and unique."
            ),
        ),
    )
    validators["validate_phone"] = field_validator(PHONE_FIELD)(validate_phone)


class UserBase(SQLModel):
    @property
    def get_valid_field(self) -> tuple[str, str]:
        """Return a tuple of a valid field and its value.\n
        The first valid field in the order of username, email,
        phone is returned. If no fields are valid, returns
        empty tuple(only for type hinting).
        """
        for key in UserBaseType.model_fields.keys():
            if key in [USERNAME_FIELD, EMAIL_FIELD, PHONE_FIELD] and getattr(
                self, key, None
            ):
                return key, getattr(self, key)
        return "", ""


UserBaseType = create_model(
    "UserBase",
    __base__=UserBase,
    __validators__=validators,
    **field_definitions,
)


def _validate(cls, value: str) -> str:
    # if len(value) < 9:
    #     raise ValueError(f"length should be at least {9}")

    if not any(char.isdigit() for char in value):
        raise ValueError("Password should have at least one numeral")

    if not any(char.isupper() for char in value):
        raise ValueError("Password should have at least one uppercase letter")

    if not any(char.islower() for char in value):
        raise ValueError("Password should have at least one lowercase letter")
    value = hash_password(value)
    return value


field_definitions = {}
field_definitions[PASSWORD_FIELD] = (
    str,
    Field(
        min_length=9,
        title="Password",
        description=(
            "The password of the user. Must "
            "be greater than 8 characters long, "
            "have at least one uppercase letter and "
            "one lowercase letter and one number."
        ),
    ),
)
validators = {}
validators["_validate"] = field_validator(PASSWORD_FIELD)(_validate)
UserCreateType = create_model(
    "UserCreate",
    __base__=UserBaseType,
    __validators__=validators,
    **field_definitions,
)


def validate_from_db(cls, dict_values: dict) -> dict:
    if any(
        True
        for key, item in dict_values.items()
        if key in [USERNAME_FIELD, EMAIL_FIELD, PHONE_FIELD] and item
    ):
        copy_dict = copy.deepcopy(dict_values)
        for k, v in copy_dict.items():
            if not v or k not in cls.model_json_schema()["properties"].keys():
                del dict_values[k]
        return dict_values
    raise ValueError(
        "At least one of username, email or phone must be provided"
    )


field_definitions = {}
validators = {}
field_definitions[ID_FIELD] = (uuid.UUID, ...)
UserPublicType = create_model(
    "UserPublic",
    __base__=UserBaseType,
    __validators__=validators,
    **field_definitions,
)


validators["validate"] = model_validator(mode="before")(validate_from_db)
UserPublicDBType = create_model(
    "UserPublicDB",
    __base__=UserBaseType,
    __validators__=validators,
    **field_definitions,
)
field_definitions = {}
UserBaseDBType = create_model(
    "UserBaseDB",
    __base__=UserBaseType,
    __validators__=validators,
    **field_definitions,
)
