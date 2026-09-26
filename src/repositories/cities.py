from sqlalchemy import update
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.db import get_read_session, get_cud_session
from src.repositories.base import BaseRepository
from src.models.cities import CityModel

class CityRepository(BaseRepository[CityModel]):
    model = CityModel

    async def delete(self, obj_id: UUID) -> None:
        await self.db.execute(update(self.model).where(self.model.id == obj_id).values(is_deleted=True))
        await self.db.flush()

def get_city_read_repository(db: AsyncSession = Depends(get_read_session)) -> CityRepository:
    return CityRepository(db)

def get_city_cud_repository(db: AsyncSession = Depends(get_cud_session)) -> CityRepository:
    return CityRepository(db)
