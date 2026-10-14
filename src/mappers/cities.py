from uuid import UUID

from src.models.cities import CityModel
from src.models.stations import StationModel
from src.schemas.cities import CityCreate, CityRead, CityUpdate
from src.schemas.stations import StationCreate, StationRead, StationUpdate

class CityMapper:
    def to_read_schema(self, orm_obj: CityModel) -> CityRead:
        return CityRead.model_validate(orm_obj)

    def to_create(self, dto: CityCreate) -> CityModel:
        return CityModel(**dto.model_dump(exclude={'stations'}))

    def to_update(self, dto: CityUpdate) -> CityModel:
        return CityModel(**dto.model_dump(exclude={'stations'}))

    def to_read_station(self, orm_obj: StationModel) -> StationRead:
        return StationRead.model_validate(orm_obj)

    def to_create_station(self, dto: StationCreate, city_id: UUID) -> StationModel:
        return StationModel(**dto.model_dump(), city_id=city_id)

    def to_update_station(self, dto: StationUpdate, city_id: UUID) -> StationModel:
        return StationModel(**dto.model_dump(exclude={'id'}), city_id=city_id)
