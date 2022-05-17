import datetime

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
    today = timezone.now()
    end_date = today + timezone.timedelta(days=3)
    logger.info(f'Every day tasks was started...')
    tasks_active = Task.objects.filter(planned_date__range=(today, end_date))
    tasks_expired = Task.objects.filter(planned_date__lte=today).exclude(status='Finished')
    logger.info(f'Find {len(tasks_active)} active tasks')
    logger.info(f'Find {len(tasks_expired)} expired tasks')
    for task in tasks_active:
        subject = f'Reminder about task {task.id}'
        message = f'Deadline of your task {task.name} is {task.planned_date}'
        users = task.executor
        logger.info(f'Send email, subject: {subject},'
                    f'message: {message},'
                    f'users: {users}')
        # email = EmailMessage(subject, message, to=[users])
        # email.send()
    for task in tasks_expired:
        subject = f'Your task {task.id} has expired!'
        message = f'Deadline of your task {task.name} was {task.planned_date}!' \
                  f'Change data or finish task!'
        users = task.executor
        logger.info(f'Send email, subject: {subject},'
                    f'message: {message},'
                    f'users: {users}')
        # email = EmailMessage(subject, message, to=[users])
        # email.send()
    logger.info(f'Tasks finished')
