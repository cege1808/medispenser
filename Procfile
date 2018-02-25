web: gunicorn medispenser.wsgi:application --log-file -
web2: daphne medispenser.asgi:application --port 8000 --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2