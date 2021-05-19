import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticket_locator.settings')

app = Celery('ticket_locator')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
