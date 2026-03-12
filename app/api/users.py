from logging import getLogger
from typing import Annotated, Sequence

from aiohttp import request
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import db_helper
from app.schemas.user import UserSchema
from app.crud import users_crud


router = APIRouter(prefix='/users', tags=['Users'])

log =  getLogger(__name__)


@router.get('/', name='users')
async def get_all_users(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
) -> Sequence[UserSchema]:
    log.info('you get all users list')
    users_list = await users_crud.get_all_users(session)
    return list(map(lambda user: UserSchema.model_validate(user), users_list))


@router.post('/register')
async def add_fastapi_users_attrs(req: Request):
    tg_user_data = await req.json()
    tg_user_data['id'] = 10
    tg_user_data['password'] = 'pass'
    tg_user_data['email'] = f'{tg_user_data["telegram_id"]}@telegram.tg'
    tg_user_data['is_active'] = True
    tg_user_data['is_superuser'] = False
    tg_user_data['is_verified'] = False
    async with request('POST', 'http://127.0.0.1:8000/register', json=tg_user_data) as req:
        res = await req.read()
    return res
