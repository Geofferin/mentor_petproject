from src.models.stations import StationModel
from src.mappers.cities import CityMapper
from src.schemas.stations import StationRead


def get_station_mapper() -> CityMapper:
    return CityMapper(StationModel, StationRead)
