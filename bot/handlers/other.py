from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiohttp import request

from bot.bot_core.bot_log_cofig import bot_logger
from bot.bot_core.config import settings
from bot.keyboards.keyboards import reply_keyboard
from bot.lexicon.lexicon_ru import BOT_BTN, BOT_INFO

other_router: Router = Router()


@other_router.message(CommandStart())
async def startup(msg: Message):
    await msg.answer('Для входа на сайт нажмите кнопку ниже 👇', reply_markup=reply_keyboard)


@other_router.message(F.text == BOT_BTN['get_info'])
async def get_user_data(msg: Message):
    user_info = msg.from_user.model_dump_json(
        include={'id', 'is_bot', 'first_name', 'last_name', 'username', 'language_code'}
    )
    async with request('POST', settings.outer_url, json=user_info) as req:
        await req.json()
    await msg.answer('Данные для регистрации переданы. Добро пожаловать!', reply_markup=ReplyKeyboardRemove())

@other_router.message(Command('info'))
async def startup(msg: Message):
    await msg.answer(BOT_INFO['description']+'\nДля входа на сайт нажмите кнопку ниже 👇', reply_markup=reply_keyboard)


@other_router.message()
async def echo(msg: Message):
    if msg.text:
        bot_logger.info(f'Поступило сообщение: {msg.text}')
        await msg.answer(msg.text)
