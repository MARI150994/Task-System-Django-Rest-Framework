from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Project, Task
from .permissions import IsManagerOrReadOnly, IsProjectOwnerOrReadOnly, IsOwnerHeadExecutorOrReadOnly
from .serializers import ProjectListSerializer, ProjectDetailSerializer, TaskSerializer, SubTaskSerializer


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    permission_classes = [IsAuthenticated & IsManagerOrReadOnly]


# can change project only owner or admin
class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated & IsProjectOwnerOrReadOnly]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Project.objects.filter(pk=pk).prefetch_related('tasks')


# tasks in project level, can create only managers
class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated & IsManagerOrReadOnly]

    # only task with generale tasks(created by manager, not subtask)
    def get_queryset(self):
        project_pk = self.kwargs.get('pk')
        return Task.objects.filter(project__pk=project_pk).filter(level=0)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {'project_id': self.kwargs.get('pk'),
             'creator_id': self.request.user.id}
        )
        return context


# task can change only who create it, executor, and had of executor
class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated & IsOwnerHeadExecutorOrReadOnly]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


# task in subtask level, can create anyone who authorized
class SubtaskList(generics.ListCreateAPIView):
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_pk = self.kwargs.get('pk')
        return Task.objects.filter(parent_id=task_pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        task_id = self.kwargs.get('pk')
        task = get_object_or_404(Task, pk=task_id)
        project = task.project
        context.update(
            {'parent_id': task_id,
             'project': project,
             'creator_id': self.request.user.id}
        )
        return context
