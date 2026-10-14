from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from typing import Annotated


class StationCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: Annotated[str, Field(min_length=1, max_length=256)]
    address: Annotated[str, Field(min_length=1, max_length=256)]
    type: Annotated[str, Field(min_length=1, max_length=256)]


class StationUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id: UUID | None = None
    name: Annotated[str, Field(min_length=1, max_length=256)]
    address: Annotated[str, Field(min_length=1, max_length=256)]
    type: Annotated[str, Field(min_length=1, max_length=256)]


class StationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    address: str
    type: str
