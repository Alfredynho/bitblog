web: gunicorn config.wsgi:application
worker: celery worker --app=warpptest.taskapp --loglevel=info
