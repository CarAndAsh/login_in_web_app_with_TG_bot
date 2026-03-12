__all__ = ('api_router',)

from fastapi import APIRouter

from .users import router
from .auth import fastapi_users_router
from app.core.app_config import settings

api_router = APIRouter(prefix=settings.api.api)
api_router.include_router(router)
api_router.include_router(fastapi_users_router)
