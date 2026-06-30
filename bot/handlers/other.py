from logging import getLogger

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from bot.keyboards.keyboards import reply_keyboard
from bot.lexicon.lexicon_ru import BOT_INFO

other_router: Router = Router()

log = getLogger(__name__)

@other_router.message(CommandStart())
async def startup(msg: Message) -> None:
    await msg.answer('Для входа на сайт нажмите кнопку ниже 👇', reply_markup=reply_keyboard)


@other_router.message(Command('info'))
async def info(msg: Message) -> None:
    await msg.answer(BOT_INFO['description']+'\nДля входа на сайт нажмите кнопку ниже 👇', reply_markup=reply_keyboard)


@other_router.message()
async def echo(msg: Message) -> None:
    if msg.text:
        log.info(f'Поступило сообщение: {msg.text}')
        await msg.answer(msg.text)
