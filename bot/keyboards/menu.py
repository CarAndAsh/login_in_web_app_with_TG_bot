from aiogram.types import BotCommand

from bot.lexicon.lexicon_ru import BOT_MENU

command_list = [BotCommand(command=cmd, description=desc) for cmd, desc in BOT_MENU.items()]
