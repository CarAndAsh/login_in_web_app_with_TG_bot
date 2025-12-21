from asyncio import run

from aiogram import Bot, Dispatcher

from bot_core.config import settings
from bot_core.log_cofig import logger
from handlers.other import other_router
from lexicon.lexicon_ru import BOT_INFO

logger.name = __file__


async def name_and_desc_check_and_set(bot: Bot):
    bot_name = await bot.get_my_name()
    bot_short_desc = await bot.get_my_short_description()
    bot_desc = await bot.get_my_description()
    if bot_name != (name := BOT_INFO['name']):
        await bot.set_my_name(name)
    if bot_short_desc != (short_desc := BOT_INFO['short_desc']):
        await bot.set_my_short_description(short_desc)
    if bot_desc != (desc := BOT_INFO['desc']):
        await bot.set_my_description(desc)


async def main():
    bot = Bot(settings.tg_bot.token, short_descripton='Базовый бот')
    logger.info('Конфигурация загружена')
    await name_and_desc_check_and_set(bot)
    dp = Dispatcher()
    dp.include_router(other_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logger.debug('Бот запущен')
    run(main())
