import os
import dj_database_url

from dotenv import load_dotenv
from .base import *


load_dotenv()

DEBUG = False

SECRET_KEY = os.getenv('SECRET_KEY')

DATABASES['default'] = dj_database_url.config(
    default={
        'DATABASE_URL':os.getenv('DATABASE_URL'),
        'REDISCLOUD_URL': os.getenv('REDISCLOUD_URL')
        },conn_max_age=600, ssl_require=True)
