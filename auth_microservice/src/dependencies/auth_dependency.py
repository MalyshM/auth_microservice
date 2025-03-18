from fastapi import HTTPException, Request

from ..logger import base_logger
from ..token_utils import verify_access_token


async def auth_dependency(request: Request) -> bool:
    base_logger.info("Auth dependency")
    try:
        # json_resp = await auth(request)
        cookies = request.cookies
        payload = (
            verify_access_token(cookies["access_token"])
            if cookies.get("access_token")
            else None
        )
        return bool(payload)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error: {e}")
