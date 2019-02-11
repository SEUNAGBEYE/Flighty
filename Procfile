web: gunicorn flighty.wsgi --log-file -
worker: celery -A config worker --beat --loglevel=info