from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.models.cities import CityModel
from src.schemas.cities import CityCreate

router = APIRouter(prefix="/cities", tags=["Города"])


@router.post('')
async def create_city(
        city_data: CityCreate = Body(...),
        db: AsyncSession = Depends(get_session)
):
    new_city = CityModel(name=city_data.name, country=city_data.country)
    db.add(new_city)
    await db.commit()
    return {'status': 'ok', 'data': new_city}
