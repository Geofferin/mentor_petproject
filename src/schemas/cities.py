from pydantic import BaseModel
from typing import Optional

class CityCreate(BaseModel):
    name: str
    country: str
