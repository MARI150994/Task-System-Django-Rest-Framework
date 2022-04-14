from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from .models import Project, Task


class TaskShortSerializer(serializers.HyperlinkedModelSerializer):
    # project = serializers.HyperlinkedRelatedField(view_name='project-detail', read_only=True)

    class Meta:
        model = Task
        fields = ['name', 'description', 'planned_date', 'project', 'priority']


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    # project = serializers.HyperlinkedRelatedField(view_name='project-detail', read_only=True)

    class Meta:
        model = Task
        fields = ['name', 'description', 'url', 'executor', 'planned_date', 'finish_date', 'priority', 'status', 'project',
                  'parent', 'children']

    def update(self, instance, validated_data):
        # if status of task was changed call function
        if validated_data.get('status'):
            if instance.status != validated_data['status']:
                instance.change_status(validated_data['status'])
        return super().update(instance, validated_data)


class SubTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        parent_id = self.context['parent_id']
        validated_data['parent_id'] = parent_id
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


class ProjectDetailSerializer(serializers.HyperlinkedModelSerializer):
    if not isinstance(serializers.CurrentUserDefault(), AnonymousUser):
        user = serializers.CurrentUserDefault()


    class Meta:
        model = Project
        fields = ['name', 'description', 'priority', 'planned_date', 'finish_date', 'manager', 'start_date', 'status',
                  'tasks']
        read_only_fields = ['tasks', 'finish_date']

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