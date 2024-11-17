from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from settings import CELERY_BROKER_URL
# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning.settings')

app = Celery('course', broker=CELERY_BROKER_URL)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
