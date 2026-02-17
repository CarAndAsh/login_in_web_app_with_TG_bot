from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    query = await session.scalars(select(User).order_by(User.id))
    return query.all()
