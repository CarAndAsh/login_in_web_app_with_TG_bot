import os
from logging import getLogger, DEBUG, Formatter, StreamHandler, FileHandler
from sys import stdout

from bot.bot_core.config import settings, BASE_DIR

formatter = Formatter(fmt=settings.log.log_format)
formatter.default_msec_format = settings.log.log_msec_format

stream = StreamHandler(stdout)
stream.setFormatter(formatter)

if 'logs' not in os.listdir(BASE_DIR):
    os.mkdir(BASE_DIR / 'logs')
to_file = FileHandler(BASE_DIR / 'logs' / '.bot_log.txt', 'w', encoding='utf-8')
to_file.setFormatter(formatter)

bot_logger = getLogger('bot_loger')
bot_logger.level = DEBUG
bot_logger.addHandler(stream)
bot_logger.addHandler(to_file)
