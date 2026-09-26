from uuid import UUID
from fastapi import Depends

from schemas.cities import CityUpdate
from src.mappers.cities import CityMapper, get_city_mapper
from src.repositories.cities import CityRepository, get_city_read_repository, get_city_cud_repository
from src.schemas.cities import CityCreate, CityRead


class CityService:
    def __init__(self, read_repository: CityRepository, cud_repository: CityRepository, mapper: CityMapper):
        self.read_repository = read_repository
        self.cud_repository = cud_repository
        self.mapper = mapper

    async def get_by_id(self, city_id: UUID) -> CityRead | None:
        city = await self.read_repository.get_by_id(city_id)
        return self.mapper.to_read_schema(city)

    async def create(self, city_data: CityCreate) -> CityRead:
        new_city = await self.cud_repository.create(**self.mapper.to_create_kwargs(city_data))
        return self.mapper.to_read_schema(new_city)

    async def update(self, city_id: UUID, city_data: CityUpdate) -> None:
        await self.cud_repository.update(city_id, **self.mapper.to_update_kwargs(city_data))

    async def delete(self, city_id: UUID) -> None:
        await self.cud_repository.delete(city_id)

def get_city_service(read_repository: CityRepository = Depends(get_city_read_repository),
                     cud_repository: CityRepository = Depends(get_city_cud_repository),
                     mapper: CityMapper = Depends(get_city_mapper)) -> CityService:
    return CityService(read_repository, cud_repository, mapper)
