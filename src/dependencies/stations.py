from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_read_session, get_cud_session
from src.models.stations import StationModel
from src.repositories.base import BaseRepository
from src.mappers.cities import CityMapper
from src.schemas.stations import StationRead


def get_station_repository_read(db: AsyncSession = Depends(get_read_session)) -> BaseRepository[StationModel]:
    return BaseRepository(db, StationModel)

def get_station_repository_cud(db: AsyncSession = Depends(get_cud_session)) -> BaseRepository[StationModel]:
    return BaseRepository(db, StationModel)

def get_station_mapper() -> CityMapper:
    return CityMapper(StationModel, StationRead)
