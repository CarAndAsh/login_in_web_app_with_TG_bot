from functools import singledispatch
from typing import Annotated

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager
from fastapi_users.authentication import JWTStrategy
from starlette.datastructures import FormData

from app.api.dependencies.authentication import get_user_manager, get_jwt_strategy
from app.api.auth import current_user
from app.core.app_config import settings
from app.models import User
from app.schemas.forms import LoginDataForm, RegisterDataForm, UserForm
from app.schemas.user import CreateUserSchema, PartialUpdateUserSchema


router = APIRouter(include_in_schema=True, tags=['User_page',])


@singledispatch
async def get_user(user_data: LoginDataForm, user_manager: BaseUserManager):
    return await user_manager.authenticate(
        OAuth2PasswordRequestForm(username=user_data.email, password=user_data.password))


@get_user.register
async def _(user_data: RegisterDataForm, user_manager: BaseUserManager):
    user = CreateUserSchema(**user_data.model_dump(exclude_none=True))
    await user_manager.create(user, safe=True)
    return await user_manager.authenticate(
        OAuth2PasswordRequestForm(username=user_data.email, password=user_data.password))


@get_user.register
async def _(user_data: CreateUserSchema, user_manager: BaseUserManager):
    user = await user_manager.create(user_data, safe=True)
    return await user_manager.authenticate(
        OAuth2PasswordRequestForm(username=user.email, password=user.password))


async def response_with_auth_cookie(req, strategy, user, user_email) -> RedirectResponse:
    response = RedirectResponse(req.url_for('user_page', email_or_tg_id=user_email))
    token = await strategy.write_token(user)
    response.set_cookie(key=settings.cookie.name, value=token)
    return response


@router.post('/auth_and_redirect_to_user_page', name='auth_redirect')
async def auth_and_redirect_to_user_page(
        req: Request,
        user_manager: Annotated[BaseUserManager, Depends(get_user_manager)],
        strategy: Annotated[JWTStrategy, Depends(get_jwt_strategy)],
):
    user_data: FormData = await req.form()
    if not user_data:
        user_data = await req.json()
        valid_user_data = CreateUserSchema.model_validate(user_data)
    elif user_data['submit'] == 'Войти':
        valid_user_data = LoginDataForm.model_validate(dict(user_data))
    elif user_data['submit'] == 'Зарегистрироваться':
        valid_user_data = RegisterDataForm.model_validate(dict(user_data))
    user = await get_user(valid_user_data, user_manager)
    return await response_with_auth_cookie(req, strategy, user, user.email)


@router.post('/update_and_redirect_to_user_page', name='update_redirect')
async def update_and_redirect_to_user_page(
        req: Request,
        user_data: Annotated[PartialUpdateUserSchema, Form()],
        user_manager: Annotated[BaseUserManager, Depends(get_user_manager)],
        user: Annotated[User, Depends(current_user)],
        strategy: Annotated[JWTStrategy, Depends(get_jwt_strategy)]
):
    user = await user_manager.update(user_update=user_data, user=user)
    return await response_with_auth_cookie(req, strategy, user, user_data.email)


# must be last in route's list because of gen path
@router.post('/{email:str}', name='user_page')
async def get_user_data(req: Request, user: Annotated[User, Depends(current_user)]):
    form = UserForm(req)
    for field in form:
        if field.name not in ('password', 'confirm_password', 'submit'):
            field.data = getattr(user, f'{field.name}')
    return settings.templates.TemplateResponse(req, 'user_page.html', {'user_form':form, 'user': user})


@router.delete('/delete_cookie')
async def delete_cookie(req: Request):
    response = RedirectResponse(req.url_for('main'))
    response.delete_cookie(settings.cookie.name)
    return response
