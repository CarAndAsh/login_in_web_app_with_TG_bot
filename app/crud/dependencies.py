from typing import Annotated, AsyncGenerator, TYPE_CHECKING

from fastapi.params import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import select

from app.models import User, db_helper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

async def get_user_email_by_tg_id(
        session: Annotated['AsyncSession', Depends(db_helper.session_getter)],
        user_tg_id: int) -> str | None:
    query = await session.execute(select(User.email).filter(User.telegram_id == user_tg_id))
    return query.scalar_one_or_none()


async def get_user_by_email(
        session: Annotated['AsyncSession', Depends(db_helper.session_getter)],
        user_email: str) -> str | None:
    query = await session.execute(select(User).filter(User.email == user_email))
    res: User | None  = query.scalar_one_or_none()
    return res


async def get_users_db(
        session: Annotated['AsyncSession', Depends(db_helper.session_getter)]
) -> AsyncGenerator['AsyncSession', None]:
    yield SQLAlchemyUserDatabase(session, User)
