__all__ = ('api_router',)

from fastapi import APIRouter

from .users import router
from .fastapi_users_routes import fastapi_users_router

api_router = APIRouter()
api_router.include_router(router)
api_router.include_router(fastapi_users_router)
