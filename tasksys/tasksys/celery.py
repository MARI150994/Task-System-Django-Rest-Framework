import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tasksys.settings')

celery_app = Celery('tasksys')
celery_app.config_from_object('django.conf:settings',
                              namespace='CELERY')
# add additional config celery beat
celery_app.autodiscover_tasks(related_name='tasks_beat')
