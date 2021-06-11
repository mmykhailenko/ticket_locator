FROM python:latest
WORKDIR /app
ENV PYTHONUNBUFFERED 1
#COPY hello_world app/hello_world
#RUN mkdir static
#COPY ticket_locator app/ticket_locator
COPY entrypoint.sh app/entrypoint.sh
#COPY manage.py app/manage.py
COPY static .
COPY wait-for-it.sh .
COPY requirements.txt .
#COPY README.md README.md
COPY . .
RUN pip install --upgrade pip
RUN chmod +x wait-for-it.sh && chmod +x app/entrypoint.sh && pip install -r requirements.txt
