import json
from logging import getLogger
from typing import Annotated

from fastapi import Request, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import get_user_by_tg_id
from app.models import db_helper
from app.schemas.user import ReadUserSchema, UserSchema
from app.crud import users_crud

router = APIRouter(prefix='/users', tags=['Users'])

log =  getLogger(__name__)

@router.post('/', name='user_page', response_model=ReadUserSchema)
async def add_user_data_by_tg_bot(req: Request, session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    user_data = await req.json()
    user_data = json.loads(user_data)
    user_data['telegram_id'] = user_data.pop('id')
    user = await users_crud.create_user(session, user_data)
    return user


@router.get('/', name='users', response_model=list[UserSchema])
async def get_all_users(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    log.info('you get all users list')
    return await users_crud.get_all_users(session)


@router.get('/{tg_id:int}', name='user_by_telegram_id', response_model=ReadUserSchema | None)
async def user_page_by_tg_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        tg_id: int
):
    user = await get_user_by_tg_id(session, tg_id)
    return user

@router.patch('/user/', name='update_some_user_data_by_telegram_id')
async def part_update_user_by_tg_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_data: Annotated[UserSchema, Depends(get_user_by_tg_id)],
        user_update: PartialUpdateUserSchema
) -> UserSchema:
    user = await users_crud.update_user(session, user_data, user_update, partial=True)
    return UserSchema.model_validate(user)


@router.put('/user/', name='update_user_data_by_telegram_id')
async def update_user_by_tg_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_data: Annotated[UserSchema, Depends(get_user_by_tg_id)],
        user_update: UpdateUserSchema
) -> UserSchema:
    user = await users_crud.update_user(session, user_data, user_update)
    return UserSchema.model_validate(user)


@router.delete('/user/', name='delete_user_by_telegram_id')
async def delete_user_by_tg_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_data: Annotated[UserSchema, Depends(get_user_by_tg_id)]
) -> None:
    await users_crud.delete_user(session, user_data)