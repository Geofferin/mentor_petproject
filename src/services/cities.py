from uuid import UUID

from src.mappers.cities import Mapper
from src.repositories.cities import CityRepository
from src.schemas.cities import CityCreate, CityRead, CityUpdate
from src.exceptions import NotFoundError


class CityService:
    def __init__(self, repository: CityRepository, mapper: Mapper):
        self.repository = repository
        self.mapper = mapper


    async def get_existing(self, city_id: UUID):
        city = await self.repository.get_by_id(city_id)
        if not city or city.is_deleted:
            raise NotFoundError(f'Did not find City with this id: {city_id}')
        return city


    async def get(self, city_id: UUID) -> CityRead:
        city = await self.get_existing(city_id)
        return self.mapper.to_read_schema(city)


    async def get_many(self, offset: int, limit: int) -> list[CityRead]:
        cities = await self.repository.get_all(offset, limit)
        result = [self.mapper.to_read_schema(city) for city in cities]
        return result


    async def create(self, city_data: CityCreate) -> CityRead:
        city_model = self.mapper.to_create(city_data)
        new_city = (await self.repository.create([city_model]))[0]
        return self.mapper.to_read_schema(new_city)


    async def update(self, city_id: UUID, city_data: CityUpdate) -> None:
        existing_city = await self.get_existing(city_id)
        updated_city = self.mapper.to_update(existing_city, city_data)
        await self.repository.update([updated_city])


    async def delete(self, city_id: UUID) -> None:
        await self.get_existing(city_id)
        await self.repository.delete([city_id])
