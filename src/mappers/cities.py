from src.models.cities import CityModel
from src.models.stations import StationModel
from src.schemas.cities import CityCreate, CityRead


class Mapper:
    def to_read_schema(self, orm_obj: CityModel) -> CityRead:
        return CityRead.model_validate(orm_obj)


    def to_create(self, dto: CityCreate) -> CityModel:
        result = CityModel(name=dto.name, country=dto.country, population=dto.population)
        result.stations = [StationModel(name=station.name, address=station.address, type=station.type)
                           for station in dto.stations]
        return result


    def to_update(self, existing_obj, new_dto) -> CityModel | StationModel:
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
