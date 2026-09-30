from sqlalchemy import update
from uuid import UUID
from src import exceptions

from src.repositories.base import BaseRepository
from src.models.cities import CityModel

class CityRepository(BaseRepository[CityModel]):
    model = CityModel

    async def delete(self, obj_id: UUID) -> None:
        if not await self.db.get(self.model, obj_id):
            raise exceptions.NotFoundError
        await self.db.execute(update(self.model).where(self.model.id == obj_id).values(is_deleted=True))
        await self.db.flush()
