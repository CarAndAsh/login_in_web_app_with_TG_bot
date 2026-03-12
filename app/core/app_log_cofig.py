import os
from sys import stdout

from app.core.app_config import settings, APP_DIR

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
        'stdout_stream': {
            'class': 'logging.StreamHandler',
            'stream': stdout,
            'formatter': 'formatter'
        },
        'to_file': {
            'class': 'logging.FileHandler',
            'filename': APP_DIR / 'logs' / '.app_log.txt',
            'mode': 'w',
            'encoding': 'utf-8',
            'formatter': 'formatter'
        }
    },
    'loggers':
        {
            'app.core.authentication.user_manager': {
                'level': settings.log.log_level_value,
                'handlers': ['stdout_stream', 'to_file'],
            },
            'app.api.users': {
                'level': settings.log.log_level_value,
                'handlers': ['stdout_stream', 'to_file'],
            },
            'app.create_app': {
                'level': settings.log.log_level_value,
                'handlers': ['stdout_stream', 'to_file'],
            },
            'uvicorn': {
                'level': settings.log.log_level_value,
                'handlers': ['stdout_stream', 'to_file'],
            },
            'uvicorn.access': {
                'level': settings.log.log_level_value,
                'handlers': ['stdout_stream'],
            }
        }

}
