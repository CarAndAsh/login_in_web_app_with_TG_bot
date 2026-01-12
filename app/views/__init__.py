__all__ = ('views_router',)

from fastapi import APIRouter

from app.views.user_page import router

views_router = APIRouter()
views_router.include_router(router)
