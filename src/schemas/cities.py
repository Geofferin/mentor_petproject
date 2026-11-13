from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from typing import Annotated

from src.schemas.stations import StationRead, StationCreate, StationUpdate


class CityCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    name: Annotated[str, Field(min_length=1, max_length=256)]
    country: Annotated[str, Field(min_length=1, max_length=256)]
    population: Annotated[int, Field(ge=0)]
    stations: Annotated[list[StationCreate], Field(min_length=1, max_length=10)]


class CityUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    name: Annotated[str, Field(min_length=1, max_length=256)]
    country: Annotated[str, Field(min_length=1, max_length=256)]
    population: Annotated[int, Field(ge=0)]
    stations: Annotated[list[StationUpdate], Field(min_length=1, max_length=10)] | None = None


class CityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    country: str
    population: int
    stations: list[StationRead] = []
