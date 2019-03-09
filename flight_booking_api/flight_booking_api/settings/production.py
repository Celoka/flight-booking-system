import os
import dj_database_url

from dotenv import load_dotenv
from .base import *


load_dotenv()

DEBUG = False

SECRET_KEY = os.getenv('SECRET_KEY')

print("I am here, from production seetings")

DATABASES['default'] = dj_database_url.config(default=os.getenv('DATABASE_URL'),
                                            conn_max_age=600, ssl_require=True)
