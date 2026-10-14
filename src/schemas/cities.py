from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from typing import Annotated

from src.schemas.stations import StationRead, StationCreate, StationUpdate


class CityCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: Annotated[str, Field(min_length=1, max_length=256)]
    country: Annotated[str, Field(min_length=1, max_length=256)]
    population: Annotated[int, Field(ge=0)]
    stations: list[StationCreate] = []


class CityUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: Annotated[str, Field(min_length=1, max_length=256)]
    country: Annotated[str, Field(min_length=1, max_length=256)]
    population: Annotated[int, Field(ge=0)]
    stations: list[StationUpdate] | None = None


class CityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    country: str
    population: int
    stations: list[StationRead] = []
