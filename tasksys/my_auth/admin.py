from django.contrib import admin
from .models import Employee, Role, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'id')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'department', 'is_header', 'is_manager')
    list_filter = ('department', 'is_header', 'is_manager')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
