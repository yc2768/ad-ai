from fastapi import APIRouter

from app.api.v1.endpoints import ad_copy, health

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(ad_copy.router)
