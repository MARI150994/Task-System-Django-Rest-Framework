from .models import Employee, Role, Department
from rest_framework import serializers


class EmployeeShortDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'url']


class EmployeeDetailSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'birthday', 'gender', 'phone', 'role', ]


class EmployeeShortSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'role']


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    employees = EmployeeShortDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ['name', 'url', 'employees']

    def create(self, validated_data):
        department_id = self.context['department_id']
        validated_data['department_id'] = department_id
        return Role.objects.create(**validated_data)


class DepartmentListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields = ['name', 'description', 'url']


class DepartmentDetailSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ['name', 'description', 'roles']
