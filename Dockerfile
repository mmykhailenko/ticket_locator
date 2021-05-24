FROM python:3.8-slim-buster

WORKDIR /ticket_locator

COPY requirements.txt requirements.txt

RUN apt update && apt install -y gcc libpq-dev python3-dev

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python", "manage.py" , "runserver"]