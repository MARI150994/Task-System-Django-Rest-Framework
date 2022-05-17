from django.utils import timezone

from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey


# abstract class for Task and Project
from .tasks import send_mail_task


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

    def save(self, *args, **kwargs):
        if not self.status:
            self.status = 'In work'
        return super().save(*args, **kwargs)

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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    executor = models.ForeignKey(get_user_model(),
                                 on_delete=models.PROTECT,
                                 verbose_name='Executor of this task',
                                 related_name='tasks')
    # time when executor select 'task in await'
    start_await_date = models.DateTimeField(null=True, blank=True)
    # it will be calculated when task 'closed' or 'finished'
    active_time = models.DurationField(null=True, blank=True)
    passive_time = models.DurationField(null=True, blank=True)
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
                if self.passive_time:
                    self.active_time = self.finish_date - self.start_date - self.passive_time
                else:
                    self.active_time = self.finish_date - self.start_date
            if self.status == 'Awaiting':
                if self.passive_time:
                    self.active_time = self.start_await_date - self.start_date - self.passive_time
                else:
                    self.active_time = self.start_await_date - self.start_date
        if new_status == 'Awaiting':
            self.start_await_date = timezone.now()
        if new_status == 'In work' and self.status == 'Awaiting':
            self.passive_time = timezone.now() - self.start_await_date
            self.start_await_time = None
        # restart project after closed
        if new_status == 'In work':
            self.finish_date = None
            self.active_time = None

    class Meta:
        ordering = ['-start_date']

    class MPTTMeta:
        order_insertion_by = ['name']
