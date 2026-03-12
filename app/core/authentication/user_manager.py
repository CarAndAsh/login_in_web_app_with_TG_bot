from logging import getLogger
from typing import TYPE_CHECKING, Optional

from fastapi_users import BaseUserManager, IntegerIDMixin

from app.core.app_config import settings
from app.models import User

if TYPE_CHECKING:
    from fastapi import Request

log = getLogger(__name__)

class UserManager(IntegerIDMixin ,BaseUserManager[User, int]):
    reset_password_token_secret = settings.jwt_strategy.secret
    verification_token_secret = settings.jwt_strategy.secret

    async def on_after_register(self, user: User, req: Optional['Request']=None) -> None:
        log.info(f'Пользователь {user.username} зарегистрирован')

    async def on_after_request_verify(self, user: User, token: str, req: Optional['Request']=None) -> None:
        log.info(f'Запрос на подтверждение для пользователя {user.username} с токеном - {token}')

    async def on_after_verify(self, user: User, req: Optional['Request']=None) -> None:
        log.info(f'Пользователь {user.username} подтвержден')

    async def on_after_delete(self, user: User, req: Optional['Request']=None) -> None:
        log.info(f'Пользователь {user.username} удален')