web1: gunicorn medispenser.wsgi:application --log-file -
web: daphne medispenser.asgi:application --port $PORT --bind 0.0.0.0 -v2