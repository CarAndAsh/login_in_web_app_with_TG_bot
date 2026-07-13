from logging import getLogger, config as logger_config

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage

from bot.bot_core.bot_log_cofig import log_config_dict
from bot.bot_core.config import settings
from bot.handlers import router
from bot.keyboards.menu import command_list
from bot.lexicon.lexicon_ru import BOT_INFO

# TODO something with recording logs in both files
log = getLogger(__name__)
logger_config.dictConfig(log_config_dict)


async def name_and_desc_check_and_set(bot: Bot) -> None:
    bot_name = await bot.get_my_name()
    bot_short_desc = await bot.get_my_short_description()
    bot_desc = await bot.get_my_description()
    if bot_name != (name := BOT_INFO['name']):
        await bot.set_my_name(name)
    if bot_short_desc != (short_desc := BOT_INFO['short_desc']):
        await bot.set_my_short_description(short_desc)
    if bot_desc != (desc := BOT_INFO['description']):
        await bot.set_my_description(desc)
    # log.info('Произведена настройка описания бота')


async def start_bot() -> None:
    session = AiohttpSession(proxy=settings.proxy)
    bot = Bot(
        settings.reg_bot.token,
        session=session,
        short_descripton='Базовый бот')
    # await name_and_desc_check_and_set(bot)
    await bot.set_my_commands(command_list)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=False)
    log.info('Бот запущен')
    await dp.start_polling(bot)
