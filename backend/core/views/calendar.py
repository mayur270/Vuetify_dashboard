from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics

from core.models import Calendar
from core.serializers import CalendarSerializer
from core.exceptions import EndDateException
from django.shortcuts import get_object_or_404


class CalendarListCreateView(generics.ListCreateAPIView):
    """
    List/ Create Events
    """

    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CalendarSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        details = serializer.validated_data["details"]
        name = serializer.validated_data["name"]
        color = serializer.validated_data["color"]
        start = serializer.validated_data["start"]
        end = serializer.validated_data["end"]

        if end < start:
            raise EndDateException("Invalid End Date")

        new_event = Calendar(name=name, details=details,
                             start=start, end=end, color=color)

        new_event.save()
        return Response({'success': 'New Event Created'}, status=status.HTTP_201_CREATED)


class CalendarRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Read, Update or Delete an event
    """

    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    def retrieve(self, request, *args, **kwargs):
        event_id = kwargs.get('event_id')
        event = self.get_queryset().filter(id=event_id)
        event_obj = get_object_or_404(event, pk=event_id)
        serializer = self.get_serializer(event_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        event_id = kwargs.get('event_id')
        event = self.get_queryset().filter(id=event_id)
        event_obj = get_object_or_404(event, pk=event_id)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        event_obj.details = serializer.validated_data["details"]
        event_obj.name = serializer.validated_data["name"]
        event_obj.color = serializer.validated_data["color"]
        event_obj.save()
        return Response({'success': 'Event Updated'}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        event_id = kwargs.get('event_id')
        event = self.get_queryset().filter(id=event_id)
        event_obj = get_object_or_404(event, pk=event_id)
        event_obj.delete()
        return Response({'success': 'Event Deleted'}, status=status.HTTP_200_OK)
