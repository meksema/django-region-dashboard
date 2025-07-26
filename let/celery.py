import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'let.settings')

app = Celery('let')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
