#!/bin/bash
app/wait-for-it.sh dbpsql:5432
python app/manage.py createsuperuser --noinput
python app/manage.py makemigrations
python app/manage.py migrate
python app/manage.py runserver 0.0.0.0:8000