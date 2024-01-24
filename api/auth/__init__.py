from fastapi import APIRouter

from api.auth.views import router as auth_router

api = APIRouter()
api.include_router(
    router=auth_router,
    prefix="",
    tags=["Users"]
)
