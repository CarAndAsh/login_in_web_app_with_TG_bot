from fastapi.params import Depends
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy

from app.core.app_config import settings
from app.core.authentication.transport import bearer_transport
from app.core.authentication.user_manager import UserManager
from app.crud.dependencies import get_users_db

from fastapi_users.db import SQLAlchemyUserDatabase

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(settings.jwt_strategy.secret, settings.jwt_strategy.lifetime_sec)

auth_backend = AuthenticationBackend(
    name='jwt', transport=bearer_transport, get_strategy=get_jwt_strategy
)

async def get_user_manager(users_db: SQLAlchemyUserDatabase = Depends(get_users_db)):
    yield UserManager(users_db)

