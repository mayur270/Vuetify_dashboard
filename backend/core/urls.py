from django.urls import path
from core.views import (TasksGetViewSet, TasksPostViewSet,
                        TasksPutViewSet, TasksDeleteViewSet,
                        CalendarListCreateView,
                        CalendarRetrieveUpdateDeleteView
                        )


urlpatterns = [
    # Task URLs
    path('tasks/', TasksGetViewSet.as_view({'get': 'get'}), name='tasks'),
    path('create-task/', TasksPostViewSet.as_view({'post': 'post'}), name='create-task'),
    path('edit-task/<int:task_id>', TasksPutViewSet.as_view({'put': 'put'}), name='edit-task'),
    path('delete-task/<int:task_id>', TasksDeleteViewSet.as_view({'delete': 'delete'}), name='delete-task'),

    # Calendar URLs
    path('events/', CalendarListCreateView.as_view(), name='events'),
    path('events/<int:event_id>', CalendarRetrieveUpdateDeleteView.as_view(), name='events_edit_delete'),
]
