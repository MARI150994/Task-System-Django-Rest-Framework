from rest_framework import serializers

from .models import Employee, Role, Department
from task.models import Task, Project
from task.serializers import TaskSerializer, ProjectDetailSerializer


class EmployeeListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'url', 'role']


class EmployeeDetailSerializer(serializers.HyperlinkedModelSerializer):
    tasks_await = serializers.SerializerMethodField()
    tasks_work = serializers.SerializerMethodField()
    projects_await = serializers.SerializerMethodField()
    projects_work = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'birthday',
                  'gender', 'phone', 'role', 'projects_await',
                  'projects_work', 'tasks_await', 'tasks_work']

    def get_tasks_await(self, obj):
        tasks = Task.objects.filter(status='Awaiting').filter(executor=obj)
        request = self.context['request']
        ser = TaskSerializer(tasks, many=True, context={'request': request})
        return ser.data

    def get_tasks_work(self, obj):
        tasks = Task.objects.filter(status='In work').filter(executor=obj)
        request = self.context['request']
        ser = TaskSerializer(tasks, many=True, context={'request': request})
        return ser.data

    def get_projects_await(self,  obj):
        projects = Project.objects.filter(status='Awaiting').filter(manager=obj)
        request = self.context['request']
        ser = ProjectDetailSerializer(projects, many=True, context={'request': request})
        return ser.data

    def get_projects_work(self,  obj):
        projects = Project.objects.filter(status='In work').filter(manager=obj)
        request = self.context['request']
        ser = ProjectDetailSerializer(projects, many=True, context={'request': request})
        return ser.data


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    employees = EmployeeListSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ['name', 'url', 'employees']

    def create(self, validated_data):
        department_id = self.context['department_id']
        validated_data['department_id'] = department_id
        return Role.objects.create(**validated_data)


class DepartmentListSerializer(serializers.HyperlinkedModelSerializer):
    num_employees = serializers.IntegerField(read_only=True)

    class Meta:
        model = Department
        fields = ['name', 'description', 'url', 'num_employees']


class DepartmentDetailSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ['name', 'description', 'roles']
