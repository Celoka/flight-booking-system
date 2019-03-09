"""
WSGI config for flight_booking_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.getenv('ENV') == 'PRODUCTION':
    print(os.getenv('ENV'))
    setting = 'flight_booking_api.settings.production'
else:
    setting = 'flight_booking_api.settings.development'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting)

application = get_wsgi_application()
