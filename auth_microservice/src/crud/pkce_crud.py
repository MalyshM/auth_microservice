from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..models.pkce_models import PKCE, PKCEType
from .base_generic_crud import CRUD


class PKCECRUD(CRUD[PKCEType, PKCEType, PKCEType]):
    name = "PKCE"

    async def read_by_host(self, host: str, session: AsyncSession) -> PKCE:
        try:
            select_result = await session.execute(
                select(self.db_entity).where(self.db_entity.host == host)
            )
            result = select_result.scalars().one()
        except NoResultFound as e:
            self.logger.error(e)
            raise HTTPException(
                status_code=404, detail=f"{self.name} not found."
            )
        return self.entity(**result.model_dump())
