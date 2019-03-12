web: gunicorn flight_booking_api.flight_booking_api.wsgi --log-file -
worker: cd flight_booking_api && celery -A flight_booking_api worker --beat --loglevel=info
