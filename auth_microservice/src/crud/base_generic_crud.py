from abc import ABC, abstractmethod
from typing import Generic, Sequence, Type, TypeVar
from uuid import UUID
from sqlmodel import SQLModel, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException

from auth_microservice.src.models.dynamic_models import ID_FIELD

T = TypeVar("T", bound=SQLModel)
CREATE_T = TypeVar("CREATE_T", bound=SQLModel)
DB_T = TypeVar("DB_T", bound=SQLModel)


class AbstractCRUD(ABC, Generic[T, CREATE_T, DB_T]):
    def __init__(
        self,
        entity: Type[T],
        create_entity: Type[CREATE_T],
        db_entity: Type[DB_T],
    ) -> None:
        super().__init__()
        self.db_entity = db_entity
        self.entity = entity
        self.create_entity = create_entity

    @abstractmethod
    async def create(self, obj: CREATE_T, session: AsyncSession) -> T:
        pass

    @abstractmethod
    async def read(self, id: UUID, session: AsyncSession) -> T:
        pass

    @abstractmethod
    async def read_all(self, session: AsyncSession) -> Sequence[T]:
        pass

    @abstractmethod
    async def update(self, obj: T, session: AsyncSession) -> T:
        pass

    @abstractmethod
    async def delete(self, id: UUID, session: AsyncSession) -> T:
        pass


class CRUD(AbstractCRUD[T, CREATE_T, DB_T]):
    async def create(self, obj: CREATE_T, session: AsyncSession) -> T:
        try:
            async with session.begin():
                db_user = self.db_entity(**obj.model_dump())
                session.add(db_user)
        except IntegrityError as e:
            raise HTTPException(
                status_code=400, detail=f"User could not be created. {e}"
            )
        return self.entity(**db_user.model_dump())

    async def read(self, id: UUID, session: AsyncSession) -> T:
        try:
            result = await session.execute(
                select(self.db_entity).where(
                    getattr(self.db_entity, ID_FIELD) == id
                )
            )
            result = result.scalars().one()
        except NoResultFound as e:
            raise HTTPException(status_code=404, detail=f"User not found. {e}")
        return self.entity(**result.model_dump())

    async def read_all(self, session: AsyncSession) -> Sequence[T]:
        result = await session.execute(select(self.db_entity))
        result = result.scalars().all()
        rsp_list = []
        for item in result:
            rsp_list.append(
                self.entity(
                    **item.model_dump(exclude_none=True, serialize_as_any=True)
                )
            )
        return rsp_list

    async def update(self, obj: T, session: AsyncSession) -> T:
        try:
            # TODO: мб не будет работать потому что не нестед
            async with session.begin():
                await session.execute(
                    update(self.db_entity)
                    .where(
                        getattr(self.db_entity, ID_FIELD)
                        == getattr(obj, ID_FIELD)
                    )
                    .values(**obj.model_dump(exclude_none=True))
                )
                return await self.read(getattr(obj, ID_FIELD), session)
        except IntegrityError as e:
            raise HTTPException(
                status_code=400, detail=f"User could not be updated. {e}"
            )

    async def delete(self, id: UUID, session: AsyncSession) -> T:
        try:
            # TODO: мб не будет работать потому что не нестед
            async with session.begin():
                deleted_row = await self.read(id, session)
                await session.execute(
                    delete(self.db_entity).where(
                        getattr(self.db_entity, ID_FIELD) == id
                    )
                )
                return deleted_row
        except IntegrityError as e:
            raise HTTPException(
                status_code=400, detail=f"User could not be deleted. {e}"
            )
