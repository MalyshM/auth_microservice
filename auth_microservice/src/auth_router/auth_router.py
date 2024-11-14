import time

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from sqlalchemy import select

# from typing import Optional

# from logger import LOGGER
# from models import connect_db_data
# = Depends(connect_db_data
group_comparison_page_router = APIRouter(tags=["Group comparison page"])


@group_comparison_page_router.get(
    "/api/attendance_static_stud_for_teams",
    name="Plot:plot",
    status_code=status.HTTP_200_OK,
    description="""""",
)
async def attendance_static_stud_for_teams(
    id_team1: int, id_team2: int, db: AsyncSession
):
    res = await db.execute(select())
    print(res)
