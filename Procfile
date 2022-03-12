release: python manage.py migrate
web: gunicorn spekit_app.wsgi:application --log-file - --log-level debug
