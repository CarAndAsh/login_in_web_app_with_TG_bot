from logging import getLogger
import webbrowser

from aiohttp import web_exceptions, client_exceptions
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiohttp import request

from bot.bot_core.config import settings
from bot.keyboards.keyboards import reply_keyboard
from bot.lexicon.lexicon_ru import BOT_BTN, BOT_INFO

other_router: Router = Router()

log = getLogger(__name__)

@other_router.message(CommandStart())
async def startup(msg: Message) -> None:
    await msg.answer('Для входа на сайт нажмите кнопку ниже 👇', reply_markup=reply_keyboard)


@other_router.message(F.text == BOT_BTN['get_info'])
async def get_user_data(msg: Message) -> None:
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
    elif resp.status == 400:
        await msg.answer('Пользователь уже зарегистрирован в системе')
    # webbrowser.open(f'{user_data.url}')


@other_router.message(Command('info'))
async def info(msg: Message) -> None:
    await msg.answer(BOT_INFO['description']+'\nДля входа на сайт нажмите кнопку ниже 👇', reply_markup=reply_keyboard)


@other_router.message()
async def echo(msg: Message) -> None:
    if msg.text:
        log.info(f'Поступило сообщение: {msg.text}')
        await msg.answer(msg.text)
