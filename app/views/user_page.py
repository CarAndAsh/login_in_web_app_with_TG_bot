from typing import Annotated

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.authentication import get_user_manager
from app.core.app_config import settings
from app.crud.dependencies import get_user_by_tg_id, get_users_db
from app.models import db_helper
from app.schemas.forms import LoginDataForm, RegisterDataForm

router = APIRouter(include_in_schema=True, tags=['User_page',])

def user_context(
        user: dict):
        context = {'labels': {
            'telegram_id': 'телеграм ID',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Никнейм',
            'email': 'Электронная почта'
        },
            'user': user}
        return context


@router.post('/redirect_to_user_page', name='redirect_to_user_page')
def redirect_to_user_page(req: Request, user_data: Annotated[LoginDataForm, Form()]):
    return RedirectResponse(req.url_for('user_page', email=user_data.email))


@router.post('/{email:str}', name='user_page')
async def get_user_data(
        req: Request,
        user_data: Annotated[LoginDataForm, Form()],
        user_manager: Annotated[BaseUserManager, Depends(get_user_manager)]
):
    user = await user_manager.authenticate(
        OAuth2PasswordRequestForm(
            username=user_data.email,
            password=user_data.password
        )
    )
    return settings.templates.TemplateResponse(req, 'user_page.html', user_context(user.to_dict()))


router = APIRouter(include_in_schema=False, tags=['For_templates',])

@router.get('/user_page/{tg_id:int}', name='user_page')
async def user_page_by_tg_id(
        req: Request,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        tg_id: int
        ):
    user = await get_user_by_tg_id(session, tg_id)
    context = user.to_dict() or {}
    return settings.templates.TemplateResponse(req, 'user_page.html', context)
