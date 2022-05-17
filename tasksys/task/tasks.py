from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import EmailMessage

from django.utils import timezone

from .models import Task

logger = get_task_logger(__name__)


@shared_task
def send_mail_task(subject: str, message: str, users: str):
    logger.info(f'Send mail task to {users}, text: {message}, time: {timezone.now()}')
    email = EmailMessage(subject, message, to=[users])
    email.send()
    logger.info('tasks finished')


@shared_task
def reminder_task():
    logger.info(f'Every day tasks was started...')
    tasks = Task.objects.filter(planned_date__day='17')
    logger.info(f'Find {len(tasks)} tasks')
    for task in tasks:
        subject = f'Reminder abou task {task.id}'
        message = f'Deadline of your task {task.name} is {task.planned_date}'
        users = task.executor
        email = EmailMessage(subject, message, to=[users])
    logger.info(f'Tasks finished')
