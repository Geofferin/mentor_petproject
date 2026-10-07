from uuid import UUID

from src.models.cities import CityModel
from src.schemas.cities import CityUpdate
from src.mappers.cities import CityMapper
from src.repositories.cities import CityRepository
from src.schemas.cities import CityCreate, CityRead
from src.exceptions import NotFoundError


class CityService:
    def __init__(self, read_repository: CityRepository, cud_repository: CityRepository, mapper: CityMapper):
        self.read_repository = read_repository
        self.cud_repository = cud_repository
        self.mapper = mapper

    async def get_existing(self, city_id: UUID) -> CityModel:
        city = await self.read_repository.get_by_id(city_id)
        if not city:
            raise NotFoundError(f'Did not find City with this id: {city_id}')
        return city

    async def get(self, city_id: UUID) -> CityRead:
        city = await self.get_existing(city_id)
        return self.mapper.to_read_schema(city)

    async def create(self, city_data: CityCreate) -> CityRead:
        city_model = self.mapper.to_create(city_data)
        new_city = await self.cud_repository.create(city_model)
        return self.mapper.to_read_schema(new_city)

    async def update(self, city_id: UUID, city_data: CityUpdate) -> None:
        await self.get_existing(city_id)
        await self.cud_repository.update(city_id, self.mapper.to_update(city_data))

    async def delete(self, city_id: UUID) -> None:
        await self.get_existing(city_id)
        await self.cud_repository.delete(city_id)
