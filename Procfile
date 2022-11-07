release: python manage.py collectstatic && python manage.py makemigrations blog && python manage.py migrate
web: gunicorn mysite.wsgi