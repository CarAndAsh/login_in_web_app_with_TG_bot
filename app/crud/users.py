from typing import Sequence, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas.user import UpdateUserSchema, PartialUpdateUserSchema


async def create_user(session: AsyncSession, user_create: dict[str, Any]) -> User:
    user = User(**user_create)
    session.add(user)
    await session.commit()
    return user


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    query = await session.scalars(select(User).order_by(User.id))
    return query.all()


async def update_user(
        session: AsyncSession,
        user_by_tg_id: User,
        user_update: UpdateUserSchema | PartialUpdateUserSchema,
        partial:bool = False) -> User:
    for key, value in user_update.model_dump(exclude_unset=partial).items():
        setattr(user_by_tg_id, key, value)
    await session.commit()
    return user_by_tg_id



async def delete_user(session: AsyncSession, user_by_tg_id: User) -> None:
    await session.delete(user_by_tg_id)
    print('deleting user')
    await session.commit()
