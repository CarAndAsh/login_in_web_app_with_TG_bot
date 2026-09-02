from logging import getLogger
from typing import Annotated, Sequence

from fastapi import APIRouter, Depends
from fastapi.params import Body
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.crud import users_crud, get_user_email_by_tg_id, get_user_by_email
from app.models import db_helper, User
from app.schemas.user import UserSchema

router = APIRouter(prefix='/users', tags=['Users'])

log =  getLogger(__name__)


@router.get('/', name='users')
async def get_all_users(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
) -> Sequence[UserSchema]:
    log.info('you get all users list')
    users_list = await users_crud.get_all_users(session)
    return list(map(lambda user: UserSchema.model_validate(user), users_list))


@router.post('/user_email_by_tg_id')
async def get_user_email(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        telegram_id: Annotated[int, Body()],
) -> JSONResponse:
    user_email: str = await get_user_email_by_tg_id(session, telegram_id)
    return JSONResponse(content=user_email)


@router.post('/user_by_email')
async def get_user_data_by_email(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_email: Annotated[str, Body()],
) -> JSONResponse:
    user: User | None = await get_user_by_email(session, user_email)
    if user:
        return JSONResponse(content={'email':user.email, 'telegram_id': user.telegram_id})
    return JSONResponse(content={'email': None, 'telegram_id': None})