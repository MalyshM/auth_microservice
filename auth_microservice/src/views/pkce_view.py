from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.pkce_crud import PKCECRUD
from ..models.dynamic_models import ID_FIELD
from ..models.pkce_models import PKCE, PKCEType
from ..schemes.pkce_sheme import PKCE_scheme


class PKCEView:
    pkce_crud: PKCECRUD = PKCECRUD(PKCEType, PKCEType, PKCEType)

    @classmethod
    def create_rsp(cls, pkce: PKCE) -> dict:
        return pkce.model_dump(
            exclude_none=True,
            serialize_as_any=True,
            mode="json",
            exclude=set(ID_FIELD),
        )

    @classmethod
    def create_rsp_list(cls, pkce_list: Sequence[PKCE]) -> Sequence[dict]:
        return [PKCEView.create_rsp(pkce) for pkce in pkce_list]

    @classmethod
    async def create(
        cls,
        obj: PKCE_scheme,
        host: str,
        session: AsyncSession,
    ) -> dict:
        pkce = await PKCEView.pkce_crud.create(
            PKCEType(**obj.model_dump(), host=host), session
        )
        return PKCEView.create_rsp(pkce)

    @classmethod
    async def read(cls, id: UUID, session: AsyncSession) -> dict:
        pkce = await PKCEView.pkce_crud.read(id, session)
        return PKCEView.create_rsp(pkce)

    @classmethod
    async def read_by_host(cls, host: str, session: AsyncSession) -> dict:
        pkce = await PKCEView.pkce_crud.read_by_host(host, session)
        return PKCEView.create_rsp(pkce)

    @classmethod
    async def read_all(cls, session: AsyncSession) -> Sequence[dict]:
        pkces = await PKCEView.pkce_crud.read_all(session)
        return PKCEView.create_rsp_list(pkces)

    @classmethod
    async def update(
        cls,
        obj: PKCE,
        session: AsyncSession,
    ) -> dict:
        pkce = await PKCEView.pkce_crud.update(obj, session)
        return PKCEView.create_rsp(pkce)

    @classmethod
    async def delete(cls, id: UUID, session: AsyncSession) -> dict:
        pkce = await PKCEView.pkce_crud.delete(id, session)
        return PKCEView.create_rsp(pkce)
