import os
from flight_booking_api.settings.base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = 'Testing'

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('DB_NAME_TEST'),
            'USER': 'postgres',
            'HOST': '127.0.0.1',
        }
    }
