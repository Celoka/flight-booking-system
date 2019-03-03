from __future__ import absolute_import
import os
import django
from django.conf import settings
from celery import Celery


setting = 'flight_booking_api.settings.development'

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting)
django.setup()
app = Celery('flight_booking_api')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
