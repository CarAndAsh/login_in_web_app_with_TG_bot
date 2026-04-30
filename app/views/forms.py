from fastapi import APIRouter, Request
from app.core.app_config import settings
from app.schemas.forms import LoginForm, RegisterForm

router = APIRouter(include_in_schema=True, tags=['Forms_templates', ])


@router.get('/user_register')
async def user_register(
        req: Request,
):
    register_form = RegisterForm(req)
    context = {'form': register_form}
    return settings.templates.TemplateResponse(req, 'user_register_page.html', context)


@router.get('/user_login')
async def user_login(
        req: Request,
):
    login_form = LoginForm(req)
    context = {'form': login_form}
    return settings.templates.TemplateResponse(req, 'user_login_page.html', context)
