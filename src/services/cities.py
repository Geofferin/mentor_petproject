from uuid import UUID

from src.models.cities import CityModel
from src.models.stations import StationModel
from src.mappers.cities import CityMapper
from src.repositories.base import BaseRepository
from src.repositories.cities import CityRepository
from src.schemas.cities import CityCreate, CityRead, CityUpdate
from src.schemas.stations import StationUpdate
from src.exceptions import NotFoundError


class CityService:
    def __init__(self, city_read_repository: CityRepository,
                 city_cud_repository: CityRepository,
                 station_read_repository: BaseRepository[StationModel],
                 station_cud_repository: BaseRepository[StationModel],
                 mapper: CityMapper):
        self.city_read_repository = city_read_repository
        self.city_cud_repository = city_cud_repository
        self.station_read_repository = station_read_repository
        self.station_cud_repository = station_cud_repository
        self.mapper = mapper

    async def get_existing(self, city_id: UUID) -> CityModel:
        city = await self.city_read_repository.get_by_id(city_id)
        if not city:
            raise NotFoundError(f'Did not find City with this id: {city_id}')
        return city

    async def get(self, city_id: UUID) -> CityRead:
        city = await self.get_existing(city_id)
        stations = await self.station_read_repository.get_by_field('city_id', city_id)
        result = self.mapper.to_read_schema(city)
        result.stations = [self.mapper.to_read_station(station) for station in stations]
        return result

    async def get_many(self, offset: int, limit: int) -> list[CityRead]:
        cities = await self.city_read_repository.get_all(offset, limit)
        result = []
        for city in cities:
            stations = await self.station_read_repository.get_by_field('city_id', city.id)
            city_dto = self.mapper.to_read_schema(city)
            city_dto.stations = [self.mapper.to_read_station(station) for station in stations]
            result.append(city_dto)
        return result

    async def create(self, city_data: CityCreate) -> CityRead:
        city_model = self.mapper.to_create(city_data)
        new_city = await self.city_cud_repository.create(city_model)
        result = self.mapper.to_read_schema(new_city)

        stations_to_create = [self.mapper.to_create_station(station, new_city.id) for station in city_data.stations]
        if stations_to_create:
            created_stations = await self.station_cud_repository.create_many(stations_to_create)
            result.stations = [self.mapper.to_read_station(station) for station in created_stations]

        return result

    async def update(self, city_id: UUID, city_data: CityUpdate) -> None:
        await self.get_existing(city_id)
        await self.city_cud_repository.update(city_id, self.mapper.to_update(city_data))

        to_create, to_update, to_delete = await self.classify_stations(city_id, city_data.stations)

        stations_to_create = [self.mapper.to_update_station(station, city_id) for station in to_create]
        await self.station_cud_repository.create_many(stations_to_create)

        for station in to_update:
            station_to_update = self.mapper.to_update_station(station, city_id)
            await self.station_cud_repository.update(station.id, station_to_update)

        await self.station_cud_repository.delete_many(to_delete)

    async def delete(self, city_id: UUID) -> None:
        await self.get_existing(city_id)

        stations_to_delete = await self.station_read_repository.get_by_field('city_id', city_id)
        station_ids = {station.id for station in stations_to_delete}
        if station_ids:
            await self.station_cud_repository.delete_many(station_ids)

        await self.city_cud_repository.delete(city_id)

    async def classify_stations(
            self, city_id: UUID,
            stations_data: list[StationUpdate]) -> tuple[list[StationUpdate], list[StationUpdate], set[UUID]]:
        existing_stations = await self.station_read_repository.get_by_field('city_id', city_id)
        existing_ids = {station.id for station in existing_stations}
        incoming_ids = {station.id for station in stations_data if station.id is not None}

        to_delete = existing_ids - incoming_ids
        to_update = [station for station in stations_data if station.id in existing_ids]
        to_create = [station for station in stations_data if station.id is None or station.id not in existing_ids]

        return to_create, to_update, to_delete
