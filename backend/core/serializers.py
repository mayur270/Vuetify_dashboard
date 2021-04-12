from rest_framework import serializers
from .models import Tasks, Calendar


class TasksSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Tasks
        fields = ('id', 'task_name', 'description',
                  'start_date', 'deadline', 'task_status')


class CalendarSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Calendar
        fields = ('id', 'name', 'details', 'start', 'end', 'color')
