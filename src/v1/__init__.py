from fastapi import APIRouter

from src.v1.routers.cities import router as cities_router
from src.v1.routers.healthcheck import router as healthcheck_router

router = APIRouter(prefix="/v1")
router.include_router(cities_router)
router.include_router(healthcheck_router)
