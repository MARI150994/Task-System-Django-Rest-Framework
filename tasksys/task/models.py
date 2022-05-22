from django.http import HttpRequest
from django.utils import timezone

from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey

from .tasks import send_mail_task


# abstract class for Task and Project
class TaskInfo(models.Model):
    STATUS_CHOICES = (
        ('In work', 'In work'),
        ('Canceled', 'Canceled'),
        ('Finished', 'Finished'),
        ('Awaiting', 'Awaiting'),
    )

    PRIORITY_CHOICES = (
        ('Very high', 'Very important'),
        ('High', 'High'),
        ('Middle', 'Middle'),
        ('Low', 'Low'),
        ('Very low', 'Very low'),
    )

    name = models.CharField(max_length=120, unique=True)
    description = models.CharField(max_length=300)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, verbose_name='Status of project/task', blank=True)
    priority = models.CharField(max_length=40, choices=PRIORITY_CHOICES, verbose_name='Priority of project/task')
    start_date = models.DateTimeField('Time when project/task was created', auto_now_add=True)
    planned_date = models.DateTimeField('Planned end date')
    finish_date = models.DateTimeField('Time when project/task was finished', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.status:
            self.status = 'In work'
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Project(TaskInfo):
    manager = models.ForeignKey(get_user_model(),
                                on_delete=models.PROTECT,
                                related_name='projects',
                                verbose_name='Users hwo can delegate and update')
    duration = models.DurationField('Duration of project', null=True, blank=True)

    def __str__(self):
        return f'Project:{self.name}, status: {self.status}'

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})

    def change_status(self, new_status):
        # if close project
        if new_status == 'Finished' or new_status == 'Canceled':
            self.finish_date = timezone.now()
            self.duration = self.finish_date - self.start_date
        # if project start again
        if new_status == 'In work':
            self.finish_date = None
            self.duration = None

    class Meta:
        ordering = ['-start_date']


# The task need for statistics time for every task for every executor and for link to project
class Task(TaskInfo, MPTTModel):
    creator = models.ForeignKey(get_user_model(),
                                 on_delete=models.PROTECT,
                                 verbose_name='Who create this task',
                                 related_name='created_tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    executor = models.ForeignKey(get_user_model(),
                                 on_delete=models.PROTECT,
                                 verbose_name='Executor of this task',
                                 related_name='tasks')
    # time when executor select 'task in await'
    start_await_date = models.DateTimeField(null=True, blank=True)
    # it will be calculated when task 'closed' or 'finished'
    active_time = models.DurationField(null=True, blank=True, default=timezone.timedelta())
    passive_time = models.DurationField(null=True, blank=True, default=timezone.timedelta())
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return f'Task:{self.name}, executor: {self.executor}'

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})

    # calculate time if form was changed
    def change_status(self, new_status):
        if new_status == 'Finished' or new_status == 'Canceled':
            if self.status == 'In work':
                self.finish_date = timezone.now()
                self.active_time = self.finish_date - self.start_date - self.passive_time

            if self.status == 'Awaiting':
                self.finish_date = timezone.now()
                self.passive_time += self.finish_date - self.start_await_date
                self.active_time = self.start_await_date - self.passive_time - self.start_date
                self.start_await_date = None

        if new_status == 'Awaiting':
            self.start_await_date = timezone.now()

        if new_status == 'In work' and self.status == 'Awaiting':
            self.passive_time += timezone.now() - self.start_await_date
            self.start_await_date = None

        # restart project after closed
        if new_status == 'In work' and self.status in ('Canceled', 'Finished'):
            self.finish_date = None

    class Meta:
        ordering = ['-start_date']

    class MPTTMeta:
        order_insertion_by = ['name']


# send message if change or create Task and Project
@receiver(post_save, sender=Project)
@receiver(post_save, sender=Task)
def create_project_message(sender, instance, created, **kwargs):
    if created:
        if sender == Project:
            subject = f'Create new project'
            message = f'You are create new project: "{instance.name}", ' \
                      f'with planned date {instance.planned_date}.\n' \
                      f'Link: {instance.get_absolute_url()}'
            users = instance.manager.email
        else:
            subject = f'New task for you'
            message = f'You have a new task: "{instance.name}" ' \
                      f'related to the project "{instance.project.name}"\n' \
                      f'with planned date {instance.planned_date}.\n' \
                      f'Link: {instance.get_absolute_url()}'
            users = instance.executor.email
        send_mail_task(subject, message, [users])
