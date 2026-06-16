from fastapi_users.authentication import BearerTransport, CookieTransport

from app.core.app_config import settings

bearer_transport: BearerTransport = BearerTransport(tokenUrl=settings.api.bearer_token_url)
cookie_transport: CookieTransport = CookieTransport(
    cookie_name=settings.cookie.name,
    cookie_max_age=settings.cookie.max_age,
    cookie_secure=settings.cookie.secure,
    cookie_httponly=settings.cookie.httponly,
    cookie_samesite=settings.cookie.samesite,
)