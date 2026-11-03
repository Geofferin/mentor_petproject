from uuid import UUID
from sqlalchemy import update

from src.repositories.base import BaseRepository
from src.models.cities import CityModel
from src.models.stations import StationModel


class CityRepository(BaseRepository[CityModel]):
    model = CityModel

    async def delete(self, obj_ids: list[UUID]) -> None:
        await self.db.execute(update(StationModel).where(StationModel.city_id.in_(obj_ids)).values(is_deleted=True))
        await super().delete(obj_ids)
