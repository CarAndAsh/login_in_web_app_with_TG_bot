import http
from typing import Annotated, Type

from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager
from fastapi_users.authentication import JWTStrategy
from fastapi.responses import RedirectResponse

from app.api.auth import current_user
from app.core.app_config import settings
from app.api.dependencies.authentication import get_user_manager, get_jwt_strategy, auth_backend
from app.models import User
from app.schemas import LoginForm, RegisterForm, UserForm, FormTypes
from app.schemas.user import CreateUserSchema, PartialUpdateUserSchema


router = APIRouter(include_in_schema=True, tags=['Forms_templates', ])


def get_submitted_form(form_cls: Type[FormTypes]):
    async def on_request(req: Request):
        user_form: FormTypes = await form_cls.from_formdata(req)
        if await user_form.validate_on_submit():
            return user_form
        return None
    return on_request


@router.get('/user_register')
@router.post('/user_register', name='user_register')
async def user_register(
        req: Request,
        user_manager: Annotated[BaseUserManager, Depends(get_user_manager)],
        strategy: Annotated[JWTStrategy, Depends(get_jwt_strategy)],
        submitted_form: Annotated[RegisterForm, Depends(get_submitted_form(RegisterForm))],
):
    if submitted_form:
        req.cookies.pop(settings.cookie.name, None)
        user: User = await user_manager.create(CreateUserSchema.model_validate(submitted_form.data), safe=True)
        login_response = await auth_backend.login(strategy, user)
        submitted_form.submit.data = False
        return RedirectResponse(req.url_for('user_page', email=user.email), headers=login_response.headers)
    context = {'form': await RegisterForm.from_formdata(req)}
    return settings.templates.TemplateResponse(req, 'user_register_page.html', context)


@router.get('/user_login')
@router.post('/user_login', name='user_login')
async def user_login(
        req: Request,
        user_manager: Annotated[BaseUserManager, Depends(get_user_manager)],
        strategy: Annotated[JWTStrategy, Depends(get_jwt_strategy)],
        submitted_form: Annotated[LoginForm, Depends(get_submitted_form(LoginForm))],
):
    if submitted_form:
        req.cookies.pop(settings.cookie.name, None)
        user: User = await user_manager.authenticate(
            OAuth2PasswordRequestForm(
                username=submitted_form.email.data,
                password=submitted_form.password.data
            )
        )
        login_response = await auth_backend.login(strategy, user)
        return RedirectResponse(req.url_for('user_page', email=user.email), headers=login_response.headers)

        # another variant from AI
        #
        # login_response.status_code = http.HTTPStatus.SEE_OTHER
        # login_response.headers['location'] = str(req.url_for('user_page', email=user.email))
        # return login_response

    context = {'form': await LoginForm.from_formdata(req)}
    return settings.templates.TemplateResponse(req, 'user_login_page.html', context)

@router.post('/user_update', name='user_update')
async def user_update(
        req: Request,
        user: Annotated[User, Depends(current_user)],
        user_manager: Annotated[BaseUserManager, Depends(get_user_manager)],
        submitted_form: Annotated[UserForm, Depends(get_submitted_form(UserForm))],):
    if submitted_form:
        await user_manager.update(PartialUpdateUserSchema.model_validate(submitted_form.data), user, safe=True)
    return RedirectResponse(req.url_for('user_page', email=user.email))


# must be last in route's list because of gen path
@router.get('/{email:str}')
@router.post('/{email:str}', name='user_page')
async def get_user_data(
        req: Request,
        user: Annotated[User, Depends(current_user)],
):
    form = UserForm(req)
    for field in form:
        if field.name not in ('password', 'confirm_password', 'submit'):
            field.data = getattr(user, f'{field.name}')
    return settings.templates.TemplateResponse(req, 'user_page.html', {'user_form':form, 'user': user})
