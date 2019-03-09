web: cd flight_booking_api && gunicorn flight_booking_api.wsgi --log-file -
worker: celery -A flight_booking_api worker -l info
