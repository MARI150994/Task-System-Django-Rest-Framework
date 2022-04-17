from django.shortcuts import get_object_or_404
from rest_framework import generics

from .models import Project, Task
from .serializers import ProjectListSerializer, ProjectDetailSerializer, TaskSerializer, SubTaskSerializer


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    # permission_classes = [IsManagerOrReadOnly]


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    # permission_classes = [IsManagerOrReadOnly]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Project.objects.filter(pk=pk).prefetch_related('tasks')


class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    # permission_classes = [IsManagerOrReadOnly]

    # only task with generale tasks(created by manager)
    def get_queryset(self):
        project_pk = self.kwargs.get('pk')
        return Task.objects.filter(project__pk=project_pk).filter(parent__isnull=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"project_id": self.kwargs.get('pk')})
        return context


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class SubtaskList(generics.ListCreateAPIView):
    serializer_class = SubTaskSerializer

    def get_queryset(self):
        task_pk = self.kwargs.get('pk')
        return Task.objects.filter(parent_id=task_pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        task_id = self.kwargs.get('pk')
        task = get_object_or_404(Task, pk=task_id)
        project = task.project
        context.update(
            {"parent_id": task_id,
             "project": project}
        )
        return context



