from fastapi import APIRouter

from api.public.masjid import views as masjids

api = APIRouter()

api.include_router(
    masjids.router,
    prefix="/masjids",
    tags=["Masjid"]
)
