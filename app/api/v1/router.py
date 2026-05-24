from fastapi import APIRouter

from app.api.v1.endpoints import ad_copy, ad_image, ad_video, health

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(ad_copy.router)
api_router.include_router(ad_image.router)
api_router.include_router(ad_video.router)
