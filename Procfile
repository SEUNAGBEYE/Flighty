web: gunicorn flighty.wsgi --log-file -
worker: celery -A flighty worker --beat --loglevel=info