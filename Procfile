web: gunicorn medispenser.wsgi --log-file -
web2: daphne -b 0.0.0.0 -p 6379 medispenser.asgi:application