from typing import Annotated, AsyncGenerator, TYPE_CHECKING

from fastapi.params import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import select

from app.models import User, db_helper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

async def get_user_by_tg_id(
        session: Annotated['AsyncSession', Depends(db_helper.session_getter)],
        user_tg_id: int) -> User | None:
    query = await session.execute(select(User).filter(User.telegram_id == user_tg_id))
    user = query.scalar()
    return user


async def get_users_db(
        session: Annotated['AsyncSession', Depends(db_helper.session_getter)]
) -> AsyncGenerator['AsyncSession', None]:
    yield SQLAlchemyUserDatabase(session, User)
