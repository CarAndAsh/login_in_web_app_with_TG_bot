from fastapi import APIRouter, Request

from app.core.app_config import settings

router = APIRouter()

@router.get('/', name='main')
def main_page(req: Request):
    return settings.templates.TemplateResponse(req, 'main.html')