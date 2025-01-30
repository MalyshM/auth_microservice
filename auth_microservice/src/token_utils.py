import os
from typing import Optional
from fastapi import Response
import jwt
import datetime
from dotenv import load_dotenv
from .models.dynamic_models import UserPublicType
from .logger import base_logger

load_dotenv()
ID_FIELD = os.getenv("ID_FIELD", "")
ACCESS_TOKEN_EXP = int(os.getenv("ACCESS_TOKEN_EXP", "15"))
ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY", "do not use default!")
REFRESH_TOKEN_EXP = int(os.getenv("REFRESH_TOKEN_EXP", "30"))
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "do not use default!")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


def create_access_token(
    data: dict, expiration_minutes: int = ACCESS_TOKEN_EXP
) -> str:
    expiration = datetime.datetime.now(
        datetime.timezone.utc
    ) + datetime.timedelta(minutes=expiration_minutes)
    data["exp"] = expiration
    if data.get(ID_FIELD):
        data[ID_FIELD] = str(data[ID_FIELD])
    token = jwt.encode(data, ACCESS_SECRET_KEY, algorithm=ALGORITHM)
    return token


def create_refresh_token(
    data: dict, expiration_days: int = REFRESH_TOKEN_EXP
) -> str:
    expiration = datetime.datetime.now(
        datetime.timezone.utc
    ) + datetime.timedelta(days=expiration_days)
    data["exp"] = expiration
    if data.get(ID_FIELD):
        data[ID_FIELD] = str(data[ID_FIELD])
    token = jwt.encode(data, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except BaseException as e:
        base_logger.error(e)
        return None


def verify_refresh_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except BaseException as e:
        base_logger.error(e)
        return None


def refresh_access_token(response: Response, refresh_token: str) -> None:
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise Exception("Invalid refresh token.")
    new_access_token = create_access_token(data=payload)
    response.set_cookie(
        key="access_token",
        value=new_access_token,
    )


def set_cookie_tokens(
    response: Response,
    rsp_body: UserPublicType,  # type: ignore this is class, not var
):
    set_access_token_cookie(response, rsp_body)
    set_refresh_token_cookie(response, rsp_body)


def set_access_token_cookie(
    response: Response,
    rsp_body: UserPublicType,  # type: ignore this is class, not var
):
    access_token = create_access_token({ID_FIELD: getattr(rsp_body, ID_FIELD)})
    response.set_cookie(
        key="access_token",
        value=access_token,
    )


def set_refresh_token_cookie(
    response: Response,
    rsp_body: UserPublicType,  # type: ignore this is class, not var
):
    refresh_token = create_refresh_token(
        {ID_FIELD: getattr(rsp_body, ID_FIELD)}
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
    )
