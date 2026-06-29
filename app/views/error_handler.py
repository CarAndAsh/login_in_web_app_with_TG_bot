from fastapi import FastAPI, Response, Request, status, HTTPException
from fastapi_users.exceptions import UserAlreadyExists

from app.core.app_config import settings


def register_errors_handlers(app: FastAPI):
    @app.exception_handler(AttributeError)
    def handle_allow_error(req: Request, exc: AttributeError) -> Response:
        exc_context = {
        'detail': 'Неверный логин или пароль',
        'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
        }
        return settings.templates.TemplateResponse(req, 'error.html', exc_context, status_code=500)

    @app.exception_handler(UserAlreadyExists)
    def handle_allow_error(req: Request, exc: UserAlreadyExists) -> Response:
        exc_context = {
        'detail': 'Пользователь с такими данными уже существует.',
        'status_code': status.HTTP_400_BAD_REQUEST
        }
        return settings.templates.TemplateResponse(req, 'error.html', exc_context, status_code=400)

    @app.exception_handler(status.HTTP_401_UNAUTHORIZED)
    def handle_unauthorized_error(req: Request, exc: HTTPException) -> Response:
        exc_context = {
        'detail': exc.detail,
        'status_code': exc.status_code
        }
        return settings.templates.TemplateResponse(req, 'error.html', exc_context, status_code=401)
