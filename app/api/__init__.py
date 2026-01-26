__all__ = ('api_router',)

from fastapi import APIRouter

from .users import router

api_router = APIRouter()
api_router.include_router(router)
