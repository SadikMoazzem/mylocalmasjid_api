from fastapi import APIRouter

from api.public.masjid import views as masjids
from api.public.config import views as config

api = APIRouter()

api.include_router(
    masjids.router,
    prefix="/masjids",
    tags=["Masjid"]
)

api.include_router(
    config.router,
    prefix="/config",
    tags=["Config"]
)
