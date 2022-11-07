release: python manage.py makemigrations blog
release: python manage.py collectstatic
web: gunicorn mysite.wsgi --log-file -