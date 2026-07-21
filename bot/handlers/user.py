from logging import getLogger

from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove
from aiohttp import request, web_exceptions, client_exceptions

from bot.bot_core import FSMAuthUser
from bot.bot_core.config import settings
from bot.keyboards.keyboards import reply_keyboard
from bot.lexicon.lexicon_ru import BOT_BTN


user_router: Router = Router()

log = getLogger(__name__)


@user_router.message(Command('reset_fsm'))
async def reset_fsm(msg: Message, state: FSMContext) -> Message:
    await state.set_state(default_state)
    return await msg.answer('Начнем сначала', reply_markup=ReplyKeyboardRemove())


async def startup(msg: Message, state: FSMContext) -> Message:
    return await msg.answer('Для входа на сайт нажмите кнопку ниже 👇', reply_markup=reply_keyboard)
    user_data = msg.from_user.model_dump(
        include={'id', 'is_bot', 'first_name', 'last_name', 'username', 'language_code'}
    )
    user_data['telegram_id'] = user_data.pop('id')
    # TODO ask user about e-mail
    user_data['email'] = f'{user_data["telegram_id"]}@tg.org'
    # TODO change password on generated
    user_data['password'] = 'pass'
    async with request('POST', settings.user_register, json=user_data) as resp:
        try:
            resp.raise_for_status()
        except web_exceptions.HTTPException:
            await msg.answer('Ошибка связи')
        except client_exceptions.ClientResponseError:
            await msg.answer('Вы уже зарегистрированы в системе')
    if resp.status == 200:
        await msg.answer(f'Данные для регистрации переданы. Добро пожаловать! Ваш временный пароль - {user_data["password"]}', reply_markup=ReplyKeyboardRemove())
    # webbrowser.open(f'{user_data.url}')
