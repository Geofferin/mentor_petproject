from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_read_session, get_cud_session
from src.repositories.cities import CityRepository
from src.mappers.cities import CityMapper
from src.services.cities import CityService


def get_city_read_repository(db: AsyncSession = Depends(get_read_session)) -> CityRepository:
    return CityRepository(db)

def get_city_cud_repository(db: AsyncSession = Depends(get_cud_session)) -> CityRepository:
    return CityRepository(db)

def get_city_mapper() -> CityMapper:
    return CityMapper()

def get_city_service(read_repository: CityRepository = Depends(get_city_read_repository),
                     cud_repository: CityRepository = Depends(get_city_cud_repository),
                     mapper: CityMapper = Depends(get_city_mapper)) -> CityService:
    return CityService(read_repository, cud_repository, mapper)
