import os
from logging import getLogger, DEBUG, Formatter, StreamHandler, FileHandler
from sys import stdout

from bot_core.config import settings, BASE_DIR

formatter = Formatter(fmt=settings.log.log_format)
formatter.default_msec_format = settings.log.log_msec_format

stream = StreamHandler(stdout)
stream.setFormatter(formatter)

if 'logs' not in os.listdir(BASE_DIR):
    os.mkdir(BASE_DIR / 'logs')
to_file = FileHandler(BASE_DIR / 'logs' / '.log.txt', 'w', encoding='utf-8')
to_file.setFormatter(formatter)

logger = getLogger()
logger.level = DEBUG
logger.addHandler(stream)
logger.addHandler(to_file)
