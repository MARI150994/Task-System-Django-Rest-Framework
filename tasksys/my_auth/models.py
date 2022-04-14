from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


class Department(models.Model):
    name = models.CharField('Department name', max_length=120, unique=True)
    description = models.CharField('Description of department', max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    department = models.ForeignKey(Department,
                                   on_delete=models.PROTECT,
                                   verbose_name='Position department name',
                                   related_name='roles')
    name = models.CharField('Position name', max_length=30)
    is_header = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    username = None
    email = models.EmailField('email address', max_length=50, unique=True)
    birthday = models.DateField('Birthday data', blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT,
                                 verbose_name='User position',
                                 related_name='employees',
                                 blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER, null=True)
    phone = models.CharField(max_length=30, blank=True, unique=True, db_index=True, null=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


