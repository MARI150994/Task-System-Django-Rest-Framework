from django.db.models import Count
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Department, Role, Employee
from .serializers import DepartmentListSerializer, RoleSerializer, EmployeeDetailSerializer, \
    DepartmentDetailSerializer, EmployeeListSerializer
from .permissions import IsAdminOrReadOnly


class DepartmentList(generics.ListCreateAPIView):
    queryset = Department.objects.annotate(num_employees=Count('roles__employees'))
    serializer_class = DepartmentListSerializer
    permission_classes = [IsAuthenticated & IsAdminOrReadOnly]


class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentDetailSerializer
    permission_classes = [IsAuthenticated & IsAdminOrReadOnly]


class RoleList(generics.ListCreateAPIView):
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated & IsAdminOrReadOnly]

    def get_queryset(self):
        department_pk = self.kwargs.get('pk')
        return Role.objects.filter(department__pk=department_pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"department_id": self.kwargs.get('pk')})
        return context


class RoleDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated & IsAdminOrReadOnly]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Role.objects.filter(pk=pk).prefetch_related('employees')


class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeDetailSerializer
    permission_classes = [IsAuthenticated & IsAdminOrReadOnly]


class EmployeeList(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeListSerializer
    permission_classes = [IsAuthenticated & IsAdminOrReadOnly]


