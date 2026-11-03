from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_read_session, get_cud_session
from src.repositories.cities import CityRepository
from src.mappers.cities import CityMapper
from src.services.cities import CityService
from src.dependencies.stations import get_station_mapper


def get_city_repository_read(db: AsyncSession = Depends(get_read_session)) -> CityRepository:
    return CityRepository(db)

def get_city_repository_cud(db: AsyncSession = Depends(get_cud_session)) -> CityRepository:
    return CityRepository(db)

def get_city_mapper() -> CityMapper:
    return CityMapper()

def get_service_read(
        repository: CityRepository = Depends(get_city_repository_read),
        city_mapper: CityMapper = Depends(get_city_mapper),
        station_mapper: CityMapper = Depends(get_station_mapper),
) -> CityService:
    return CityService(repository, city_mapper, station_mapper)

def get_service_cud(
        repository: CityRepository = Depends(get_city_repository_cud),
        city_mapper: CityMapper = Depends(get_city_mapper),
        station_mapper: CityMapper = Depends(get_station_mapper),
) -> CityService:
    return CityService(repository, city_mapper, station_mapper)
