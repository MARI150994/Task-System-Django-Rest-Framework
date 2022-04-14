from rest_framework import routers
from django.urls import path

from . import views

urlpatterns = [
    path('', views.DepartmentList.as_view(), name='department-list'),
    path('<int:pk>', views.DepartmentDetail.as_view(), name='department-detail'),
    path('<int:pk>/roles', views.RoleList.as_view(), name='role-list'),
    path('roles/<int:pk>', views.RoleDetail.as_view(), name='role-detail'),
    path('users/', views.EmployeeList.as_view(), name='employee-list'),
    path('user/<int:pk>', views.EmployeeDetail.as_view(), name='employee-detail'),
]