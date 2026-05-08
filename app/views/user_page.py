from functools import singledispatch
from typing import Annotated, Union

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.authentication import get_user_manager
from app.core.app_config import settings
from app.crud.dependencies import get_user_by_tg_id
from app.models import db_helper
from app.schemas.forms import LoginDataForm, RegisterDataForm, UserForm
from app.schemas.user import CreateUserSchema

router = APIRouter(include_in_schema=True, tags=['User_page',])

UserFormType: Union = LoginDataForm | RegisterDataForm


@router.post('/redirect_to_user_page', name='redirect_to_user_page')
def redirect_to_user_page(req: Request, user_data: Annotated[UserFormType, Form()]):
    return RedirectResponse(req.url_for('user_page', email=user_data.email))


@singledispatch
async def get_user(user_data: LoginDataForm, user_manager: BaseUserManager):
    return await user_manager.authenticate(
        OAuth2PasswordRequestForm(username=user_data.email, password=user_data.password))


@get_user.register
async def _(user_data: RegisterDataForm, user_manager: BaseUserManager):
    user = CreateUserSchema(**user_data.model_dump(exclude_none=True))
    user = await user_manager.create(user, safe=True)
    return user


@router.post('/{email:str}', name='user_page')
async def get_user_data(
        req: Request,
        user_data: Annotated[UserFormType, Form()],
        user_manager: Annotated[BaseUserManager, Depends(get_user_manager)]
):
    user = await get_user(user_data, user_manager)
    form = UserForm(req)
    for field in form:
        if field.name not in ('password', 'confirm_password', 'submit'):
            field.data = getattr(user, f'{field.name}')
    return settings.templates.TemplateResponse(req, 'user_page.html', {'user_form':form, 'user': user})


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
