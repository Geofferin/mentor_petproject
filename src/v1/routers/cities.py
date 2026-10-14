from fastapi import APIRouter, Depends, status, Query
from uuid import UUID

from src.schemas.cities import CityCreate, CityUpdate
from src.services.cities import CityService
from src.dependencies.cities import get_city_service


router = APIRouter(prefix="/cities", tags=["Города"])

@router.get('/{city_id}', status_code=status.HTTP_200_OK)
async def get_city(city_id: UUID, service: CityService = Depends(get_city_service)):
    city = await service.get(city_id)
    return city

@router.get('', status_code=status.HTTP_200_OK)
async def get_cities(
        offset: int = Query(default=0, ge=0, description='Пропуск первых n записей'),
        limit: int = Query(default=10, gt=0, le=100, description='Кол-во записей на странице'),
        service: CityService = Depends(get_city_service)):
    cities = await service.get_many(offset, limit)
    return cities

@router.post('', status_code=status.HTTP_201_CREATED)
async def create_city(
        city_data: CityCreate,
        service: CityService = Depends(get_city_service)):
    return await service.create(city_data)

@router.put('/{city_id}', status_code=status.HTTP_204_NO_CONTENT)
async def edit_city(
        city_id: UUID,
        city_data: CityUpdate,
        service: CityService = Depends(get_city_service)):
    return await service.update(city_id, city_data)

@router.delete('/{city_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: UUID, service: CityService = Depends(get_city_service)):
    return await service.delete(city_id)
