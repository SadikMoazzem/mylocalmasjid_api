from fastapi import APIRouter

from mylocalmasjid_api.public.masjid import views as masjids
from mylocalmasjid_api.public.config import views as config

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
