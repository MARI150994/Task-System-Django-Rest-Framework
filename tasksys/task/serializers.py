from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from .models import Project, Task
from .tasks import send_mail_task


class TaskShortSerializer(serializers.HyperlinkedModelSerializer):
    # project = serializers.HyperlinkedRelatedField(view_name='project-detail', read_only=True)

    class Meta:
        model = Task
        fields = ['name', 'description', 'planned_date', 'project', 'priority']


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    # project = serializers.HyperlinkedRelatedField(view_name='project-detail', read_only=True)

    class Meta:
        model = Task
        fields = ('name', 'description', 'url', 'executor',
                  'planned_date', 'priority', 'status',
                  'project', 'parent', 'children',
                  'active_time', 'passive_time', 'start_await_date',
                  'finish_date')
        read_only_fields = ('project', 'parent', 'children', 'active_time',
                            'passive_time', 'start_await_date', 'finish_date')

    def update(self, instance, validated_data):
        # if status of task was changed call function
        if validated_data.get('status'):
            if instance.status != validated_data['status']:
                instance.change_status(validated_data['status'])
        return super().update(instance, validated_data)

    def create(self, validated_data):
        project_id = self.context['project_id']
        validated_data['project_id'] = project_id
        return Task.objects.create(**validated_data)


class SubTaskSerializer(TaskSerializer):
    class Meta(TaskSerializer.Meta):
        model = Task

    def create(self, validated_data):
        parent_id = self.context['parent_id']
        project = self.context['project']
        validated_data.update(
            {"parent_id": parent_id,
             "project": project}
        )
        return Task.objects.create(**validated_data)


class ProjectListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'priority', 'planned_date', 'manager', 'start_date', 'status', 'url']

    def validate(self, data):
        # check that the planned time more than start_time
        if data['planned_date'] <= timezone.now():
            raise serializers.ValidationError("Planned time must occur after start")
        return data

    def create(self, validated_data):
        prj = validated_data.get('name')
        planned_date = validated_data.get('planned_date')
        manager = validated_data.get('manager')
        print(manager)
        subject = f'Created project {prj}'
        message = f'You are create a new project: {prj} with planned date: {planned_date}'
        send_mail_task(subject, message, [manager])
        return super().create(validated_data)


class ProjectDetailSerializer(serializers.HyperlinkedModelSerializer):
    if not isinstance(serializers.CurrentUserDefault(), AnonymousUser):
        user = serializers.CurrentUserDefault()

    class Meta:
        model = Project
        fields = ('name', 'description', 'priority', 'planned_date',
                  'finish_date', 'manager', 'start_date', 'status',
                  'tasks', 'duration')
        read_only_fields = ('tasks', 'finish_date', 'duration')

    def update(self, instance, validated_data):
        # if status of task was changed call function
        if validated_data.get('status'):
            if instance.status != validated_data['status']:
                instance.change_status(validated_data['status'])
        return super().update(instance, validated_data)

    def validate(self, data):
        if self.partial:
            return data
        # check that the planned time more than start_time
        if data.get('planned_date') <= timezone.now():
            raise serializers.ValidationError("Planned time must occur after start")
        return data
