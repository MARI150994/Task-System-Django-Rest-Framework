from typing import List

from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import EmailMessage
from django.utils import timezone


logger = get_task_logger(__name__)


@shared_task
def send_mail_task(subject: str, message: str, users: List[str]):
    logger.info(f'Send mail task to {users}, text: {message}, time: {timezone.now()}')
    email = EmailMessage(subject, message, to=users)
    email.send()
    logger.info('tasks finished')


