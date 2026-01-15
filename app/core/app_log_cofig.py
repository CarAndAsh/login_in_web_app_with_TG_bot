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
to_file = FileHandler(BASE_DIR / 'logs' / '.app_log.txt', 'w', encoding='utf-8')
to_file.setFormatter(formatter)

app_logger = getLogger('app_loger')
app_logger.level = DEBUG
app_logger.addHandler(stream)
app_logger.addHandler(to_file)
