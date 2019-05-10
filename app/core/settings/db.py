import os

from .base import env, root

DATABASES = None

SQLITE3_DATABASE_DEFAULT_NAME = 'db.sqlite3'

if 'DEFAULT_DATABASE_URL' in env:
    DATABASES = {
        'default': env.db_url(var='DEFAULT_DATABASE_URL')
    }
else:
    # In case there is nothing in .env file. Using default sqlite3 database to prevent errors.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(root.root, SQLITE3_DATABASE_DEFAULT_NAME)
        }
    }
