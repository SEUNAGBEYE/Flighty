web: sh -c "cd flighty && gunicorn flighty.wsgi --log-file -" 
worker: celery -A flighty worker --beat --loglevel=info