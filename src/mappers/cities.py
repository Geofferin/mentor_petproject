from src.models.cities import CityModel
from src.schemas.cities import CityCreate, CityRead, CityUpdate

class CityMapper:
    def to_read_schema(self, orm_obj: CityModel) -> CityRead:
        return CityRead.model_validate(orm_obj)

    def to_create(self, dto: CityCreate) -> CityModel:
        return CityModel(**dto.model_dump())

    def to_update(self, dto: CityUpdate) -> CityModel:
        return CityModel(**dto.model_dump())
