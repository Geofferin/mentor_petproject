from collections.abc import Sequence

from src.models.cities import CityModel
from src.models.stations import StationModel
from src.schemas.cities import CityCreate, CityRead, CityUpdate


class CityMapper:
    def to_read_schema(self, orm_obj: CityModel | Sequence[CityModel]) -> CityRead | list[CityRead]:
        if isinstance(orm_obj, CityModel):
            result = CityRead.model_validate(orm_obj)
        else:
            result = [CityRead.model_validate(obj) for obj in orm_obj]
        return result


    def to_create(self, dto: CityCreate) -> CityModel:
        result = CityModel(**dto.model_dump(exclude={'stations'}))
        result.stations = [StationModel(**station.model_dump()) for station in dto.stations]
        return result


    def to_update(self, existing_obj: CityModel | StationModel, new_dto: CityUpdate | StationModel) -> CityModel:
        data = new_dto.model_dump(exclude={'id', 'stations'}, exclude_unset=True, exclude_none=True)
        for key, value in data.items():
            setattr(existing_obj, key, value)

        stations = getattr(new_dto, 'stations', None)
        if stations:
            existing_by_id = {station.id: station for station in existing_obj.stations}
            for station in stations:
                if station.id in existing_by_id:
                    self.to_update(existing_by_id[station.id], station)

        return existing_obj
