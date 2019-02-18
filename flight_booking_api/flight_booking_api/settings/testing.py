import os
from flight_booking_api.settings.base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = 'Testing'

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('DB_NAME_TEST'),
            'USER': os.getenv('DB_USER'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT')
        }
    }
