from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from typing import Annotated


class StationCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    name: Annotated[str, Field(min_length=1, max_length=256)]
    address: Annotated[str, Field(min_length=1, max_length=256)]
    type: Annotated[str, Field(min_length=1, max_length=256)]


class StationUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    id: UUID
    name: Annotated[str, Field(min_length=1, max_length=256)] | None = None
    address: Annotated[str, Field(min_length=1, max_length=256)] | None = None
    type: Annotated[str, Field(min_length=1, max_length=256)] | None = None


class StationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    address: str
    type: str
