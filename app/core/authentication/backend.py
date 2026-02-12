from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend

from app.core.app_config import settings

bearer_transport: BearerTransport = BearerTransport(tokenUrl=settings.api.bearer_token_url)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(settings.jwt_strategy.secret, settings.jwt_strategy.lifetime_sec)

auth_backend = AuthenticationBackend(
    name='jwt', transport=bearer_transport, get_strategy=get_jwt_strategy
)
