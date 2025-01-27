from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import JSONResponse

from auth_microservice.src.models.dynamic_models import ID_FIELD
from auth_microservice.src.token_utils import (
    refresh_access_token,
    verify_access_token,
    verify_refresh_token,
)


auth_router = APIRouter(tags=["Auth"])


@auth_router.get(
    "/auth",
)
async def auth(
    request: Request,
) -> Response:
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
                raise HTTPException(status_code=401, detail="Not authenticated")
            payload = verify_refresh_token(refresh_token)
            if not payload:
                raise HTTPException(status_code=401, detail="Not authenticated")
            response = JSONResponse(content=payload[ID_FIELD], status_code=200)
            refresh_access_token(response, cookies["refresh_token"])
            return response
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Error: {e}")
    else:
        return JSONResponse(content=payload[ID_FIELD], status_code=200)
