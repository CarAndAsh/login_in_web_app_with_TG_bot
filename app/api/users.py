import json
from typing import Annotated

from fastapi import Request, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import get_user_by_tg_id
from app.models import db_helper
from app.schemas.user import ReadUserSchema, UserSchema
from app.crud import users_crud

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/', name='user_page', response_model=ReadUserSchema)
async def add_user_data_by_tg_bot(req: Request, session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    user_data = await req.json()
    user_data = json.loads(user_data)
    user_data['telegram_id'] = user_data.pop('id')
    user = await users_crud.create_user(session, user_data)
    return user


@router.get('/', name='users', response_model=list[UserSchema])
async def get_all_users(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    return await users_crud.get_all_users(session)


@router.get('/{tg_id:int}', name='user_by_telegram_id', response_model=ReadUserSchema | None)
async def user_page_by_tg_id(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        tg_id: int
):
    user = await get_user_by_tg_id(session, tg_id)
    return user
