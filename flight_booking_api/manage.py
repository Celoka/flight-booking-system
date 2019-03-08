#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

load_dotenv()

if os.getenv('ENV') == 'PRODUCTION':
    setting = 'flight_booking_api.settings.production'
else:
    setting = 'flight_booking_api.settings.development'

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting)
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
