from typing import Generic, TypeVar
from pydantic import BaseModel

from src.models.base import Base
from src.models.cities import CityModel
from src.schemas.cities import CityRead


ModelType = TypeVar('ModelType', bound=Base)
ReadSchemaType = TypeVar('ReadSchemaType', bound=BaseModel)


class CityMapper(Generic[ModelType, ReadSchemaType]):
    model: type[ModelType] = CityModel
    read_schema: type[ReadSchemaType] = CityRead

    def __init__(self, model: type[ModelType] | None = None, read_schema: type[ReadSchemaType] | None = None):
        if model is not None:
            self.model = model
        if read_schema is not None:
            self.read_schema = read_schema

    def to_read_schema(self, orm_obj: ModelType) -> ReadSchemaType:
        return self.read_schema.model_validate(orm_obj)

    def to_create(self, dto, **extra_fields) -> ModelType:
        return self.model(**dto.model_dump(exclude={'id', 'stations'}), **extra_fields)

    def to_update(self, existing_obj, new_dto) -> ModelType:
        data = new_dto.model_dump(exclude={'id', 'stations'}, exclude_unset=True, exclude_none=True)
        for key, value in data.items():
            setattr(existing_obj, key, value)
        return existing_obj
