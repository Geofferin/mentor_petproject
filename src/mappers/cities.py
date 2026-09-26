from src.models.cities import CityModel
from src.schemas.cities import CityCreate, CityRead, CityUpdate

class CityMapper:
    def to_read_schema(self, orm_obj: CityModel) -> CityRead:
        return CityRead.model_validate(orm_obj)

    def to_create_kwargs(self, dto: CityCreate) -> dict:
        return dto.model_dump()

    def to_update_kwargs(self, dto: CityUpdate) -> dict:
        return dto.model_dump()

def get_city_mapper() -> CityMapper:
    return CityMapper()
