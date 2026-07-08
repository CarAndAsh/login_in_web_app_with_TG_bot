from logging import getLogger
from typing import Annotated, Sequence

from fastapi import APIRouter, Depends
from fastapi.params import Body
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.crud import users_crud
from app.crud.dependencies import get_user_email_by_tg_id
from app.models import db_helper
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