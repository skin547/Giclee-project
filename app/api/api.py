from fastapi import APIRouter

from app.api.endpoint import images

api_router = APIRouter()

api_router.include_router(images.router, prefix="/images", tags=["images"])