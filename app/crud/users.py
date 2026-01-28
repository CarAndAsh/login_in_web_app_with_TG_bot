from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


async def create_user(session: AsyncSession, user_create: dict) -> User:
    user = User(**user_create)
    session.add(user)
    await session.commit()
    return user


async def get_user(session: AsyncSession, user_id) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_tg_id(session: AsyncSession, user_tg_id) -> User | None:
    query = await session.execute(select(User).filter(User.telegram_id == user_tg_id))
    return query.scalar()


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    query = await session.scalars(select(User).order_by(User.id))
    return query.all()


async def update_user(session: AsyncSession):
    pass


async def delete_user(session: AsyncSession):
    pass
