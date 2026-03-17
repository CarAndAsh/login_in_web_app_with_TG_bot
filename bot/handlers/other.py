import json
from logging import getLogger
import webbrowser

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
    user_info = msg.from_user.model_dump(
        include={'id', 'is_bot', 'first_name', 'last_name', 'username', 'language_code'}
    )
    async with request('POST', settings.register, json=user_info) as resp:
        user_data, status = await resp.json()
        if status == 201:
            await msg.answer('Данные для регистрации переданы. Добро пожаловать!', reply_markup=ReplyKeyboardRemove())
        elif status == 400 and user_data.get('detail') == 'REGISTER_USER_ALREADY_EXISTS':
            await msg.answer('Пользователь уже зарегистрирован в системе')
        else:
            await msg.answer('Данные для регистрации переданы. Добро пожаловать!', reply_markup=ReplyKeyboardRemove())
            webbrowser.open(f'{settings.user_page}/{user_id}')


@other_router.message(Command('info'))
async def info(msg: Message) -> None:
    await msg.answer(BOT_INFO['description']+'\nДля входа на сайт нажмите кнопку ниже 👇', reply_markup=reply_keyboard)


@other_router.message()
async def echo(msg: Message) -> None:
    if msg.text:
        log.info(f'Поступило сообщение: {msg.text}')
        await msg.answer(msg.text)
