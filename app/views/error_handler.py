from fastapi import FastAPI, Response, Request, status, HTTPException

from app.core.app_config import settings


def register_errors_handlers(app: FastAPI):
    @app.exception_handler(AttributeError)
    def handle_allow_error(req: Request, exc: AttributeError) -> Response:
        exc_context = {
        'detail': 'Incorrect login or password',
        'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
        }
        return settings.templates.TemplateResponse(req, 'error.html', exc_context)

    @app.exception_handler(status.HTTP_401_UNAUTHORIZED)
    def handle_unauthorized_error(req: Request, exc: HTTPException) -> Response:
        exc_context = {
        'detail': exc.detail,
        'status_code': exc.status_code
        }
        return settings.templates.TemplateResponse(req, 'error.html', exc_context)
