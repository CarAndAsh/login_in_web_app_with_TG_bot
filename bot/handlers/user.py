from logging import getLogger

from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiohttp import request, web_exceptions

from bot.bot_core import FSMAuthUser
from bot.bot_core.config import settings
from bot.keyboards.keyboards import reply_keyboard
from bot.lexicon.lexicon_ru import BOT_BTN, STATE_INPUT_PLACEHOLDER

user_router: Router = Router()

log = getLogger(__name__)


@user_router.message(Command('reset_fsm'))
async def reset_fsm(msg: Message, state: FSMContext) -> Message:
    await state.set_state(default_state)
    return await msg.answer('Начнем сначала', reply_markup=ReplyKeyboardRemove())



@user_router.message(CommandStart(), StateFilter(default_state))
async def startup(msg: Message, state: FSMContext) -> Message:
    await state.set_state(FSMAuthUser.check_user)
    return await msg.answer('Для входа на сайт нажмите кнопку ниже 👇',reply_markup=reply_keyboard)


@user_router.callback_query(F.data == 'check_user', FSMAuthUser.check_user)
async def get_user_data(cbq: CallbackQuery, state: FSMContext) -> Message:
    user_data = cbq.from_user.model_dump(
        include={'id', 'is_bot', 'first_name', 'last_name', 'username', 'language_code'}
    )
    user_tg_id: int = user_data.pop('id')
    user_data['telegram_id'] = user_tg_id

    async with request('POST', settings.check_user_email, json=user_tg_id) as req:
        try:
            user_email = await req.json()
        except web_exceptions.HTTPException:
           return await cbq.message.edit_text('Ошибка связи')

    if user_email:
        await state.set_state(FSMAuthUser.password_fill)
        await state.set_data({'user_email':user_email})
        answer = await cbq.message.edit_text(
            f'Ваш e-mail, зарегистрированеный в системе - {user_email}. Введите пароль для входа.',
        )
    else:
        await state.set_data(user_data)
        await state.set_state(FSMAuthUser.email_fill)
        answer = await cbq.message.edit_text(
            'Ваш e-mail, не указан в системе, для регистрации укажите его в поле ввода.',
        )
    await state.update_data({'edit_msg_id':cbq.message})
    return answer


@user_router.message(FSMAuthUser.email_fill)
async def get_users_email(msg:Message, state: FSMContext):
    await state.update_data({'user_email':msg.text})
    await msg.delete()
    editable_msg = await state.get_value('edit_msg_id')
    await editable_msg.edit_text(
        'e-mail принят, теперь введите пароль',
    )


@user_router.message(FSMAuthUser.password_fill)
async def get_users_password(msg:Message, state: FSMContext):
    user_data = await state.get_data()
    user_password = msg.text
    user_data['password'] = user_password
    await msg.delete()
    editable_msg = await state.get_value('edit_msg_id')
    if 'user_email' in user_data:
        await state.set_state(FSMAuthUser.login)
        await editable_msg.edit_text(
        f'С возвращением, {msg.from_user.first_name}! Перейдите в свой профиль по ссылке ниже',
    )
    else:
        await state.set_state(FSMAuthUser.register)
        await editable_msg.edit_text(
        'Благодарим за регистрацию, перейдите в свой профиль по ссылке ниже'
    )
    # webbrowser.open(f'{user_data.url}')
