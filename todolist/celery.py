from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todolist.settings')

celery_app = Celery('todolist')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()