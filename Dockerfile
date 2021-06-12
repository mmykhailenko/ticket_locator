FROM python:latest
WORKDIR /app
ENV PYTHONUNBUFFERED 1
COPY entrypoint.sh app/entrypoint.sh
COPY static .
COPY wait-for-it.sh .
COPY requirements.txt .
COPY . .
RUN pip install --upgrade pip
RUN chmod +x wait-for-it.sh && chmod +x app/entrypoint.sh && pip install -r requirements.txt
