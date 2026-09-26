from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, TypeVar
from uuid import UUID

from src.models.base import Base

ModelType = TypeVar('ModelType', bound=Base)


class BaseRepository(Generic[ModelType]):
    model: type[ModelType]

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, obj_id: UUID) -> ModelType | None:
        result = await self.db.execute(select(self.model).where(self.model.id == obj_id))
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> ModelType:
        obj = self.model(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def update(self, obj_id: UUID, **kwargs) -> None:
        await self.db.execute(update(self.model).where(self.model.id == obj_id).values(**kwargs))
        await self.db.flush()

    async def delete(self, obj_id: UUID) -> None:
        await self.db.execute(delete(self.model).where(self.model.id == obj_id))
        await self.db.flush()
