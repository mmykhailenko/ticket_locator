#!/bin/bash
app/wait-for-it.sh database-postgres.cy2ykcv5puov.eu-central-1.rds.amazonaws.com:5432
python manage.py collectstatic --no-input
python manage.py init_admin
python manage.py makemigrations
python manage.py migrate
gunicorn ticket_locator.wsgi:application -b 0.0.0.0:8000 --reload

