web: gunicorn flight_booking_api.wsgi --log-file -
worker: celery -A flight_booking_api worker --beat --loglevel=info
