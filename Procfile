release: python manage.py collecstatic && python manage.py makemigrations blog && python manage.py migrate
web: gunicorn mysite.wsgi