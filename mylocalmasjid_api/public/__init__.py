from fastapi import APIRouter

from mylocalmasjid_api.public.masjid import views as masjids
from mylocalmasjid_api.public.config import views as config
from mylocalmasjid_api.public.health import views as health

api = APIRouter()

api.include_router(
    masjids.router,
    prefix="/masjids",
    tags=["Masjid"]
)

api.include_router(
    config.router,
    prefix="/configs",
    tags=["Config"]
)

api.include_router(
    health.router,
    prefix="/health",
    tags=["Health"]
)
