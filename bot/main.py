from asyncio import run

from aiogram import Bot, Dispatcher

from bot.core.config import settings

reg_bot = Bot(settings.reg_bot.token)
dispatcher = Dispatcher()

async def face_bot_prepare(bot: Bot):
    bot_name = await bot.get_my_name()
    bot_short_desc = await bot.get_my_short_description()
    bot_desc = await bot.get_my_description()
    if bot_name != (name := settings.reg_bot.name):
        await bot.set_my_name(name)
    if bot_short_desc != (short_desc := settings.reg_bot.short_desc):
        await bot.set_my_short_description(short_desc)
    if bot_desc != (desc := settings.reg_bot.description):
        await bot.get_my_description(desc)


async def main_func():
    await face_bot_prepare(reg_bot)
    await dispatcher.start_polling(reg_bot)

if __name__ == '__main__':
    run(main_func())