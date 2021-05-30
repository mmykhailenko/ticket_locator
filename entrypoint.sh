#!/bin/bash
app/wait-for-it.sh dbpsql:5432
python manage.py init_admin
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000