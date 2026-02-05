import os
from sys import stdout

from bot.bot_core.config import settings, BASE_DIR

if 'logs' not in os.listdir():
    os.mkdir('logs')

log_config_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'formatter': {
            'format': settings.log.log_format,
            'default_msec_format': settings.log.log_msec_format
        }
    },
    'handlers': {
        'to_bot_log_file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/.bot_log.txt',
            'mode': 'w',
            'encoding': 'utf-8',
            'formatter': 'formatter'
        },
        'stdout_stream': {
            'class': 'logging.StreamHandler',
            'stream': stdout,
            'formatter': 'formatter'
        }
    },
    'loggers':
        {
            'bot.test_bot': {
                'level': settings.log.log_level_value,
                'handlers': ['stdout_stream', 'to_bot_log_file'],
            },
            'bot.handlers.other': {
                'level': settings.log.log_level_value,
                'handlers': ['stdout_stream', 'to_bot_log_file'],
            }
        }
}
