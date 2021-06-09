FROM python:3.8.9-alpine3.13
WORKDIR /app
ENV PYTHONUNBUFFERED 1
COPY hello_world app/hello_world
COPY static app/static
COPY ticket_locator app/ticket_locator
COPY manage.py app/manage.py
COPY wait-for-it.sh app/wait-for-it.sh
COPY requirements.txt app/requirements.txt
COPY README.md README.md
RUN pip install --upgrade pip
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev && apk add bash
RUN chmod +x app/wait-for-it.sh && pip install -r app/requirements.txt
