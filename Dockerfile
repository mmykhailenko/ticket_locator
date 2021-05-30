FROM python:3.9

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ticket_locator ./ticket_locator
COPY hello_world ./hello_world
COPY manage.py ./
COPY README ./
COPY entrypoint.sh ./entrypoint.sh

RUN chmod +x ./entrypoint.sh