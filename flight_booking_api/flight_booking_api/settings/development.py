import os
from dotenv import load_dotenv
from .base import *


load_dotenv()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = 'e4gmk)8q80t^b%zf(tu^z)hdd$*femf!*c-uafw#x5!#c9#)t='

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT')
        }
    }
