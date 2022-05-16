from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import EmailMessage


logger = get_task_logger(__name__)


@shared_task
def send_mail_task(subject, message, users):
    email = EmailMessage(subject, message, to=[users])
    email.send()
