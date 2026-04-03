import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Unify_API.settings')

app = Celery('Unify_API')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()