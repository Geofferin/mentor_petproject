from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, TypeVar, Sequence
from uuid import UUID

from src.models.base import Base


ModelType = TypeVar('ModelType', bound=Base)

class BaseRepository(Generic[ModelType]):
    model: type[ModelType]

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, obj_id: UUID) -> ModelType | None:
        return await self.db.get(self.model, obj_id)

    async def get_all(self, offset: int, limit: int) -> Sequence[ModelType]:
        result = await self.db.execute(
            select(self.model)
            .where(self.model.is_deleted.is_(False))
            .offset(offset)
            .limit(limit)
            .order_by(self.model.created_at))
        return result.scalars().all()

    async def create(self, objs: list[ModelType]) -> list[ModelType]:
        self.db.add_all(objs)
        await self.db.flush()
        return objs

    async def update(self, objs: list[ModelType]) -> None:
        self.db.add_all(objs)
        await self.db.flush()

    async def delete(self, obj_ids: list[UUID]) -> None:
        await self.db.execute(update(self.model).where(self.model.id.in_(obj_ids)).values(is_deleted=True))
        await self.db.flush()
