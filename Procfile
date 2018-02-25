web: gunicorn medispenser.asgi:application --log-file -
websock: daphne medispenser.asgi:application --port $PORT --bind 0.0.0.0 -v2