from typing import Annotated

from fastapi import APIRouter, Request
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.app_config import settings
from app.crud.dependencies import get_user_by_tg_id
from app.models import db_helper

def user_context(
        user: dict):
        context = {'labels': {
            'telegram_id': 'телеграм ID',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Никнейм',
            'email': 'Электронная почта'
        },
            'user': user}
        return context


router = APIRouter(include_in_schema=False, tags=['For_templates',])

@router.get('/user_page/{tg_id:int}', name='user_page')
async def user_page_by_tg_id(
        req: Request,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        tg_id: int
        ):
    user = await get_user_by_tg_id(session, tg_id)
    context = user.to_dict() or {}
    return settings.templates.TemplateResponse(req, 'user_page.html', context)
