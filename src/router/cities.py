import datetime
from fastapi import APIRouter, Depends, Body
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.models.cities import CityModel
from src.schemas.cities import CityCreate

router = APIRouter(prefix="/cities", tags=["Города"])


@router.get('/{city_id}')
async def get_city(city_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CityModel).where(CityModel.id == city_id))
    return result.scalar_one_or_none()

@router.post('')
async def create_city(
        city_data: CityCreate = Body(...),
        db: AsyncSession = Depends(get_session)
):
    new_city = CityModel(name=city_data.name, country=city_data.country)
    db.add(new_city)
    await db.commit()
    return {'status': 'ok', 'data': new_city}

@router.put('/{city_id}')
async def edit_city(
        city_id: int,
        city_data: CityCreate = Body(...),
        db: AsyncSession = Depends(get_session)
):
    await db.execute(update(CityModel).where(CityModel.id == city_id).values(
        name=city_data.name, country=city_data.country #, updated_at=datetime.datetime.utcnow() оказалось не нужно
    ))
    await db.commit()
    return {'status': 'ok', 'data': city_data}

@router.delete('/{city_id}')
async def delete_city(city_id: int, db: AsyncSession = Depends(get_session)):
    await db.execute(update(CityModel).where(CityModel.id == city_id).values(is_deleted=True))
    # Рабочий вариант для обычного удаления
    # await db.execute(delete(CityModel).where(CityModel.id == city_id))
    await db.commit()
    return {'status': 'ok'}
