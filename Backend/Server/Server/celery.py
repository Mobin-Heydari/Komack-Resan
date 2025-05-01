import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Server.settings')

app = Celery('Server')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix in your settings.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks in your apps.
app.autodiscover_tasks()
