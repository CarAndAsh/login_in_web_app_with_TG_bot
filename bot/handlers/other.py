from logging import getLogger

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import any_state
from aiogram.types import Message

from bot.keyboards.keyboards import reply_keyboard
from bot.lexicon.lexicon_ru import BOT_INFO

other_router: Router = Router()

log = getLogger(__name__)


@other_router.message(Command('info'))
async def info(msg: Message) -> Message:
    return await msg.answer(BOT_INFO['description']+'\nДля входа на сайт нажмите кнопку ниже 👇', reply_markup=reply_keyboard)


@other_router.message(any_state)
async def delete_msg(msg: Message):
    if msg.text:
        log.info(f'Поступило сообщение: {msg.text}, и было удалено')
        return await msg.delete()
