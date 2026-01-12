from fastapi import APIRouter, Request

from app.core.config import settings

router = APIRouter(include_in_schema=False, prefix='/user_page')

@router.get('/', name='user_page')
def user_page(req: Request):
    context = {}
    return settings.templates.TemplateResponse(req, 'user_page.html', context)
