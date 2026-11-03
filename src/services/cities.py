from uuid import UUID

from src.mappers.cities import CityMapper
from src.repositories.cities import CityRepository
from src.schemas.cities import CityCreate, CityRead, CityUpdate
from src.exceptions import NotFoundError


class CityService:
    def __init__(self, repository: CityRepository, city_mapper: CityMapper, station_mapper: CityMapper):
        self.repository = repository
        self.city_mapper = city_mapper
        self.station_mapper = station_mapper


    async def get_existing(self, city_id: UUID):
        city = await self.repository.get_by_id(city_id)
        if not city:
            raise NotFoundError(f'Did not find City with this id: {city_id}')
        return city


    async def get(self, city_id: UUID) -> CityRead:
        city = await self.get_existing(city_id)
        return self.city_mapper.to_read_schema(city)


    async def get_many(self, offset: int, limit: int) -> list[CityRead]:
        cities = await self.repository.get_all(offset, limit)
        result = [self.city_mapper.to_read_schema(city) for city in cities]
        return result


    async def create(self, city_data: CityCreate) -> CityRead:
        city_model = self.city_mapper.to_create(city_data)
        city_model.stations = [self.station_mapper.to_create(station) for station in city_data.stations]
        new_city = (await self.repository.create([city_model]))[0]
        return self.city_mapper.to_read_schema(new_city)


    async def update(self, city_id: UUID, city_data: CityUpdate) -> None:
        existing_city = await self.get_existing(city_id)

        existing_stations_by_id = {station.id: station for station in existing_city.stations}
        for station in city_data.stations:
            if station.id in existing_stations_by_id:
                self.station_mapper.to_update(existing_stations_by_id[station.id], station)

        updated_city = self.city_mapper.to_update(existing_city, city_data)
        await self.repository.update([updated_city])


    async def delete(self, city_id: UUID) -> None:
        await self.get_existing(city_id)
        await self.repository.delete([city_id])
