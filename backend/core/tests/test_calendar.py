import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from core.models import Calendar


class TestCalendar(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.event_1 = Calendar.objects.create(name='Meeting with Tim',
                                               details='Working on presentation',
                                               color='red', start='2021-04-12',
                                               end='2021-05-12')
        self.event_2 = Calendar.objects.create(name='Meeting with Sophie',
                                               details='Working on excel sheets',
                                               color='blue', start='2021-05-04',
                                               end='2021-05-08')

    def teardown(self):
        Calendar.objects.all().delete()

    def test_calendar_get_view(self):
        """
        Class: CalendarListCreateView
        Desc: Getting list of all events
        """

        url = reverse('events')
        response = self.client.get(url, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(resp_obj), 2)  # Counting total events

    def test_calendar_post_view(self):
        """
        Class: CalendarListCreateView
        Desc: Creating a new event
        """

        data = {'name': 'Meeting with Sophie',
                'details': 'Working on excel sheets',
                'color': 'blue',
                'start': '2021-05-04',
                'end': '2021-05-08'}
        url = reverse('events')
        response = self.client.post(url, data, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 201)
        self.assertEquals(resp_obj, {'success': 'New Event Created'})

    def test_calendar_post_view_enddate(self):
        """
        Class: CalendarListCreateView
        Desc: End date should greater than/ equal to start date
        """

        data = {'name': 'Meeting with Sophie',
                'details': 'Working on excel sheets',
                'color': 'blue',
                'start': '2021-05-04',
                'end': '2021-04-08'}
        url = reverse('events')
        response = self.client.post(url, data, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 400)
        self.assertEquals(resp_obj, {'detail': 'Invalid End Date'})

    def test_calendar_edit_view(self):
        """
        Class: CalendarRetrieveUpdateDeleteView
        Desc: Editing/ Updating an event
        """

        data = {'name': self.event_1.name,
                'details': 'Design a system',
                'start': self.event_1.start,
                'end': self.event_1.end,
                'color': self.event_1.color}
        url = reverse('events_edit_delete', args=[self.event_1.id])
        response = self.client.put(url, data, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(resp_obj, {'success': 'Event Updated'})

    def test_calendar_delete_view(self):
        """
        Class: CalendarRetrieveUpdateDeleteView
        Desc: Deleting an event
        """

        # Checking if its deleted
        url = reverse('events_edit_delete', args=[self.event_1.id])
        response = self.client.delete(url, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(resp_obj, {'success': 'Event Deleted'})

        # Checking if the deleted event exists
        response = self.client.get(url, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 404)
        self.assertEquals(resp_obj, {'detail': 'Not found.'})
