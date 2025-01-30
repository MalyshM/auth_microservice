from typing import Optional
from fastapi import HTTPException, Request
from ..logger import base_logger
from ..routers.auth_router import auth


async def auth_dependency(request: Request) -> Optional[str]:
    base_logger.info("Auth dependency")
    try:
        json_resp = await auth(request)
        return json_resp.headers.get("Set-Cookie")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error: {e}")
