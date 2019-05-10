from .base import root, os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standart': {
            'format': '%(asctime)s [%(levelname)s]: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'standart'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'standart',
            'filename': os.path.join(root.root, 'adjust-app.log'),
        }
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG'
        },
        # This one is for local debug only.
        # 'django': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG'
        # }
    }
}
