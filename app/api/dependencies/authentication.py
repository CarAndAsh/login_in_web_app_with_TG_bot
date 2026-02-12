from typing import TYPE_CHECKING

from fastapi.params import Depends
from sqlalchemy.sql.annotation import Annotated

from app.core.authentication.user_manager import UserManager
from app.crud.dependencies import get_users_db

if TYPE_CHECKING:
    from fastapi_users.db import SQLAlchemyUserDatabase


async def get_user_manager(users_db: Annotated['SQLAlchemyUserDatabase', Depends(get_users_db)]):
    yield UserManager(users_db)
