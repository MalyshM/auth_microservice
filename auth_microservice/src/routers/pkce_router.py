from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.pkce_models import PKCE, PKCEType
from ..schemes.pkce_sheme import PKCE_scheme
from ..views.pkce_view import PKCEView
from ..connection import connect_db_data
from ..docs.responses import (
    create_response_400,
    delete_response_400,
    response_401,
    response_404,
    update_response_400,
)
from ..models.dynamic_models import UserPublicDBType


pkce_router = APIRouter(
    prefix="/pkce",
    tags=["PKCE"],
    responses={401: response_401},
)


@pkce_router.post(
    "",
    summary="Create a New PKCE",
    description="Creates a new PKCE entry in the system.",
    response_model=PKCE,
    response_model_exclude_none=True,
    responses={
        400: create_response_400,
    },
)
async def post_pkce(
    request: Request,
    pkce: PKCE_scheme,
    session: AsyncSession = Depends(connect_db_data),
) -> JSONResponse:
    res = await PKCEView.create(pkce, request.headers["host"], session)
    return JSONResponse(content=res, status_code=200)


@pkce_router.get(
    "",
    summary="Get All PKCE Entries",
    description="Retrieves a list of all PKCE entries in the system.",
    response_model=Sequence[PKCE],
    response_model_exclude_none=True,
)
async def get_pkces(
    request: Request,
    session: AsyncSession = Depends(connect_db_data),
) -> JSONResponse:
    res = await PKCEView.read_all(session)
    return JSONResponse(content=res, status_code=200)


@pkce_router.get(
    "/{pkce_id}",
    summary="Get PKCE by ID",
    description="Retrieves a PKCE entry by its unique ID.",
    response_model=PKCEType,
    response_model_exclude_none=True,
    responses={
        404: response_404,
    },
)
async def get_pkce(
    request: Request,
    pkce_id: str,
    session: AsyncSession = Depends(connect_db_data),
) -> JSONResponse:
    res = await PKCEView.read(UUID(pkce_id), session)
    return JSONResponse(content=res, status_code=200)


@pkce_router.post(
    "/pkce_by_host",
    summary="Get PKCE by Host",
    description="Retrieves PKCE entries based on a specific host.",
    response_model=PKCEType,
    response_model_exclude_none=True,
)
async def pkce_by_host(
    request: Request,
    host: str,
    session: AsyncSession = Depends(connect_db_data),
) -> JSONResponse:
    res = await PKCEView.read_by_host(host, session)
    return JSONResponse(content=res, status_code=200)


@pkce_router.put(
    "/{pkce_id}",
    summary="Update PKCE Entry",
    description="Updates the information of an existing PKCE entry.",
    response_model=PKCEType,
    response_model_exclude_none=True,
    responses={
        400: update_response_400,
        404: response_404,
    },
)
async def update_pkce(
    request: Request,
    user: UserPublicDBType,  # type: ignore # this is class, not var
    session: AsyncSession = Depends(connect_db_data),
) -> JSONResponse:
    res = await PKCEView.update(user, session)
    return JSONResponse(content=res, status_code=200)


@pkce_router.delete(
    "/user/{pkce_id}",
    summary="Delete PKCE Entry",
    description="Deletes a PKCE entry from the system by its unique ID.",
    response_model=PKCEType,
    responses={
        400: delete_response_400,
        404: response_404,
    },
)
async def delete_pkce(
    request: Request,
    pkce_id: str,
    session: AsyncSession = Depends(connect_db_data),
) -> JSONResponse:
    res = await PKCEView.delete(UUID(pkce_id), session)
    return JSONResponse(content=res, status_code=200)
