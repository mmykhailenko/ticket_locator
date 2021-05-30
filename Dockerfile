FROM python:latest
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY hello_world hello_world/
COPY ticket_locator ticket_locator/
COPY templates templates/
COPY manage.py manage.py
COPY wait-for-it.sh wait-for-it.sh
COPY entrypoint.sh entrypoint.sh
COPY README.md README.md
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN chmod +x wait-for-it.sh && chmod +x entrypoint.sh && pip install -r requirements.txt
ENTRYPOINT ["./entrypoint.sh"]