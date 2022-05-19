from rest_framework import routers
from django.urls import path

from . import views


urlpatterns = [
  path('projects/', views.ProjectList.as_view(), name='project-list'),
  path('projects/<int:pk>/', views.ProjectDetail.as_view(), name='project-detail'),
  path('projects/<int:pk>/tasks/', views.TaskList.as_view(), name='task-list'),
  path('<int:pk>/', views.TaskDetail.as_view(), name='task-detail'),
  path('<int:pk>/delegate/', views.SubtaskList.as_view(), name='subtasks'),
]