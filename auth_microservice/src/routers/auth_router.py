import json

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..connection import connect_db_data
from ..docs.responses import auth_200, auth_403, response_401
from ..models.dynamic_models import ID_FIELD
from ..password_utils import generate_code_challenge
from ..routers.pkce_router import pkce_by_host, post_pkce
from ..schemes.pkce_sheme import PKCE_scheme
from ..token_utils import (
    refresh_access_token,
    verify_access_token,
    verify_refresh_token,
)

auth_router = APIRouter(tags=["Auth"])


@auth_router.post(
    "/auth",
    summary="Authenticate User",
    description=(
        "Authenticates the user by verifying the access token or "
        "refreshing it using the refresh token."
    ),
    responses={
        200: auth_200,
        401: response_401,
        403: auth_403,
    },
)
async def auth(
    request: Request,
    pkce_sheme: PKCE_scheme,
    session: AsyncSession = Depends(connect_db_data),
) -> Response:
    """
    Authenticates the user by checking the access token or refreshing it using
    the refresh token.

    ### Steps:
    1. Checks if the `access_token` is present in the cookies and validates it.
    2. If the `access_token` is invalid or expired, it checks for a
    `refresh_token`.
    3. If the `refresh_token` is valid, a new `access_token` is generated
    and returned.
    4. If neither token is valid, an HTTP 401 Unauthorized error is returned.

    ### Parameters:
    - **request**: The incoming HTTP request containing cookies.

    ### Returns:
    - **JSONResponse**: The user GUID if authentication is successful.
    - **HTTPException**: 401 Unauthorized if authentication fails.
    """
    if pkce_sheme.is_to_check():
        code = generate_code_challenge(pkce_sheme.code_verifier or "")
        pkce_res = await pkce_by_host(
            request, request.headers["host"], session
        )
        assert isinstance(pkce_res.body, bytes)
        pkce_dict = json.loads(pkce_res.body.decode("utf-8"))
        if code != pkce_dict["code_challenge"]:
            raise HTTPException(403, "Send true code_verifier")
    else:
        await post_pkce(request, pkce_sheme, session)
    cookies = request.cookies
    payload = (
        verify_access_token(cookies["access_token"])
        if cookies.get("access_token")
        else None
    )
    if not payload:
        try:
            refresh_token = (
                cookies["refresh_token"]
                if cookies.get("refresh_token")
                else None
            )
            if not refresh_token:
                raise HTTPException(
                    status_code=401, detail="Not authenticated"
                )
            payload = verify_refresh_token(refresh_token)
            if not payload:
                raise HTTPException(
                    status_code=401, detail="Not authenticated"
                )
            response = JSONResponse(content=payload[ID_FIELD], status_code=200)
            refresh_access_token(response, cookies["refresh_token"])
            return response
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Error: {e}")
    else:
        return JSONResponse(content=payload[ID_FIELD], status_code=200)
