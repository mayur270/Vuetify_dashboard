from rest_framework import viewsets, status
from rest_framework.response import Response
from core.models import Tasks
from core.serializers import TasksSerializer
from django.shortcuts import get_object_or_404
from core.exceptions import EndDateException


class TasksGetViewSet(viewsets.ViewSet):
    """
    List of all Tasks
    """

    def get(self, request, *args, **kwargs):
        queryset = Tasks.objects.all()
        serializer = TasksSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TasksPostViewSet(viewsets.ViewSet):
    """
    Creating New Task
    """

    def post(self, request, *args, **kwargs):
        serializer = TasksSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task_name = serializer.validated_data["task_name"]
        description = serializer.validated_data["description"]
        start_date = serializer.validated_data["start_date"]
        deadline = serializer.validated_data["deadline"]
        task_status = serializer.validated_data["task_status"]

        if deadline < start_date:
            raise EndDateException("Invalid End Date")

        new_task = Tasks(task_name=task_name, description=description,
                         start_date=start_date, deadline=deadline,
                         task_status=task_status)

        new_task.save()
        return Response({'success': 'New Task Created'}, status=status.HTTP_201_CREATED)


class TasksPutViewSet(viewsets.ViewSet):
    """
    Editing a Task
    """

    def put(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        task = Tasks.objects.filter(id=task_id)
        task_obj = get_object_or_404(task, pk=task_id)

        serializer = TasksSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task_obj.task_name = serializer.validated_data["task_name"]
        task_obj.description = serializer.validated_data["description"]
        task_obj.start_date = serializer.validated_data["start_date"]
        task_obj.deadline = serializer.validated_data["deadline"]
        task_obj.task_status = serializer.validated_data["task_status"]

        if task_obj.deadline < task_obj.start_date:
            raise EndDateException("Invalid End Date")

        task_obj.save()
        return Response({'success': ''}, status=status.HTTP_200_OK)


class TasksDeleteViewSet(viewsets.ViewSet):
    """
    Deleting a Task
    """

    def delete(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        task = Tasks.objects.filter(id=task_id)
        task_obj = get_object_or_404(task, pk=task_id)
        task_obj.delete()
        return Response({'success': ''}, status=status.HTTP_200_OK)
