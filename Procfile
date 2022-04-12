release: python manage.py migrate
web: gunicorn soccer_app.wsgi:application --log-file - --log-level debug
