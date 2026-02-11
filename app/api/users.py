import json
from logging import getLogger
from typing import Annotated, Sequence

from fastapi import Request, APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import db_helper
from app.schemas.user import UserSchema, UpdateUserSchema, PartialUpdateUserSchema, CreateUserSchema
from app.crud import users_crud, get_user_by_tg_id


router = APIRouter(prefix='/users', tags=['Users'])

log =  getLogger(__name__)


@router.post('/', name='user_page')
async def add_user_data_by_tg_bot(
        req: Request, session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
)-> Response:
    user_data = await req.json()
    user_data = json.loads(user_data)
    user_tg_id = user_data.pop('id')
    user_data['telegram_id'] = user_tg_id
    user_for_response = await get_user_by_tg_id(session, user_tg_id)
    response = Response()
    if not user_for_response:
        await users_crud.create_user(session, user_data)
    else:
        response.headers['user_tg_id'] = str(user_for_response.telegram_id)
    return response


@router.get('/', name='users')
async def get_all_users(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
) -> Sequence[UserSchema]:
    log.info('you get all users list')
    users_list = await users_crud.get_all_users(session)
    return list(map(lambda user: UserSchema.model_validate(user), users_list))


@router.get('/{tg_id:int}/', name='user_by_telegram_id')
async def user_page_by_tg_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        tg_id: int
) -> UserSchema:
    user = await get_user_by_tg_id(session, tg_id)
    return UserSchema.model_validate(user)


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