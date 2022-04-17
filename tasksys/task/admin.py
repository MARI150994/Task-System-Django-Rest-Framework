from django.contrib import admin
from .models import Project, Task


@admin.register(Project)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'id')


@admin.register(Task)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'id')
