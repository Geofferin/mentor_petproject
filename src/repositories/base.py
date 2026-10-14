from sqlalchemy import update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, TypeVar, Sequence
from uuid import UUID

from src.models.base import Base


ModelType = TypeVar('ModelType', bound=Base)

class BaseRepository(Generic[ModelType]):
    model: type[ModelType]

    def __init__(self, db: AsyncSession, model: type[ModelType] | None = None):
        self.db = db
        if model is not None:
            self.model = model

    async def get_by_id(self, obj_id: UUID) -> ModelType | None:
        return await self.db.get(self.model, obj_id)

    async def get_by_field(self, field_name: str, value) -> Sequence[ModelType]:
        column = getattr(self.model, field_name)
        result = await self.db.execute(select(self.model).where(column == value))
        return result.scalars().all()

    async def get_all(self, offset: int, limit: int) -> Sequence[ModelType]:
        result = await self.db.execute(select(self.model).offset(offset).limit(limit).order_by(self.model.created_at))
        return result.scalars().all()

    async def create(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def create_many(self, objs: list[ModelType]) -> list[ModelType]:
        self.db.add_all(objs)
        await self.db.flush()
        return objs

    async def update(self, obj_id: UUID, obj: ModelType) -> None:
        existing = await self.db.get(self.model, obj_id)

        for column in self.model.__table__.columns:
            if column.name in ('id', 'city_id', 'created_at', 'updated_at', 'is_deleted'):
                continue
            setattr(existing, column.name, getattr(obj, column.name))

        await self.db.flush()

    async def delete(self, obj_id: UUID) -> None:
            await self.db.execute(delete(self.model).where(self.model.id == obj_id))
            await self.db.flush()

    async def delete_many(self, obj_ids: set[UUID]) -> None:
        await self.db.execute(update(self.model).where(self.model.id.in_(obj_ids)).values(is_deleted=True))
        await self.db.flush()
