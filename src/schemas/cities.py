from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Annotated


class CityCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: Annotated[str, Field(min_length=1, max_length=256)]
    country: Annotated[str, Field(min_length=1, max_length=256)]
    population: Annotated[int, Field(ge=0)]


class CityUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: Annotated[str, Field(min_length=1, max_length=256)]
    country: Annotated[str, Field(min_length=1, max_length=256)]
    population: Annotated[int, Field(ge=0)]


class CityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    country: str
    population: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
