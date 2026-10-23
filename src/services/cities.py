from uuid import UUID

from src.models.cities import CityModel
from src.models.stations import StationModel
from src.mappers.cities import CityMapper
from src.repositories.base import BaseRepository
from src.repositories.cities import CityRepository
from src.schemas.cities import CityCreate, CityRead, CityUpdate
from src.exceptions import NotFoundError


class CityService:
    def __init__(self, city_repository: CityRepository,
                 station_repository: BaseRepository[StationModel],
                 city_mapper: CityMapper,
                 station_mapper: CityMapper):
        self.city_repository = city_repository
        self.station_repository = station_repository
        self.city_mapper = city_mapper
        self.station_mapper = station_mapper


    async def get_existing(self, city_id: UUID) -> CityModel:
        city = await self.city_repository.get_by_id(city_id)
        if not city:
            raise NotFoundError(f'Did not find City with this id: {city_id}')
        return city


    async def get(self, city_id: UUID) -> CityRead:
        city = await self.get_existing(city_id)
        stations = await self.station_repository.get_by_field('city_id', city_id)
        result = self.city_mapper.to_read_schema(city)
        result.stations = [self.station_mapper.to_read_schema(station) for station in stations]
        return result


    async def get_many(self, offset: int, limit: int) -> list[CityRead]:
        cities = await self.city_repository.get_all(offset, limit)
        result = []
        for city in cities:
            stations = await self.station_repository.get_by_field('city_id', city.id)
            city_dto = self.city_mapper.to_read_schema(city)
            city_dto.stations = [self.station_mapper.to_read_schema(station) for station in stations]
            result.append(city_dto)
        return result


    async def create(self, city_data: CityCreate) -> CityRead:
        city_model = self.city_mapper.to_create(city_data)
        new_city = await self.city_repository.create(city_model)
        result = self.city_mapper.to_read_schema(new_city)

        stations_to_create = [self.station_mapper.to_create(station, city_id = new_city.id) for station in city_data.stations]
        if stations_to_create:
            created_stations = await self.station_repository.create_many(stations_to_create)
            result.stations = [self.station_mapper.to_read_schema(station) for station in created_stations]

        return result


    async def update(self, city_id: UUID, city_data: CityUpdate) -> None:
        existing_city = await self.get_existing(city_id)
        updated_city = self.city_mapper.to_update(existing_city, city_data)
        await self.city_repository.update([updated_city])

        if city_data.stations:
            existing_stations = {
                station.id: station
                for station in await self.station_repository.get_by_field('city_id', city_id)}
            stations_to_update = [station for station in city_data.stations if station.id in existing_stations]
            if stations_to_update:
                stations = [self.station_mapper.to_update(
                    existing_stations[station.id],
                    station)
                    for station in stations_to_update]
                await self.station_repository.update(stations)


    async def delete(self, city_id: UUID) -> None:
        await self.get_existing(city_id)

        stations_to_delete = await self.station_repository.get_by_field('city_id', city_id)
        station_ids = {station.id for station in stations_to_delete}
        if station_ids:
            await self.station_repository.delete_many(station_ids)

        await self.city_repository.delete(city_id)
