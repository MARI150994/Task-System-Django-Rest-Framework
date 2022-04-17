from .models import Employee, Role, Department
from rest_framework import serializers


class EmployeeListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email']


class EmployeeDetailSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'birthday', 'gender', 'phone', 'role', ]


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
