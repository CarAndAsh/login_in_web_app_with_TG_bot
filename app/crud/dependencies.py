from typing import Annotated

from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, db_helper


async def get_user_by_tg_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_tg_id: int) -> User | None:
    query = await session.execute(select(User).filter(User.telegram_id == user_tg_id))
    user = query.scalar()
    return user
