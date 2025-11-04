#!/bin/sh

python3 manage.py collectstatic --noinput
python3 maange.py makemigrations --noinput
python3 manage.py migrate --noinput
gunicorn --bind 0.0.0.0:8081 --workers 3 service.wsgi:application