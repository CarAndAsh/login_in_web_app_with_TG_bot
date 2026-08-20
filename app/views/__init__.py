__all__ = ('views_router',)

from fastapi import APIRouter

from app.views.user_page import router as user_page_router
from app.views.forms import router as forms_router
from app.views.other import router as other_router

views_router = APIRouter(tags=['Views'])
views_router.include_router(forms_router)
views_router.include_router(user_page_router)
views_router.include_router(other_router)