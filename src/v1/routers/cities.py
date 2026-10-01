from fastapi import APIRouter, Depends, status
from uuid import UUID

from schemas.cities import CityUpdate
from src.schemas.cities import CityCreate
from src.services.cities import CityService
from src.dependencies.cities import get_city_service


router = APIRouter(prefix="/cities", tags=["Города"])

@router.get('/{city_id}', status_code=status.HTTP_200_OK)
async def get_city(city_id: UUID, service: CityService = Depends(get_city_service)):
    city = await service.get_by_id(city_id)
    return city

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
