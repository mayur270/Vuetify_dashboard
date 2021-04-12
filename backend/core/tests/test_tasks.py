import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from core.models import Tasks


class TestTasks(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.task_1 = Tasks.objects.create(task_name='Drawing',
                                           description='Draw different shapes',
                                           task_status='Not Started',
                                           start_date='2021-04-12',
                                           deadline='2021-05-12')

        self.task_2 = Tasks.objects.create(task_name='Painting',
                                           description='Paint all four walls',
                                           task_status='Not Started',
                                           start_date='2021-04-15',
                                           deadline='2021-04-20')

    def teardown(self):
        Tasks.objects.all().delete()

    def test_tasks_get_view(self):
        """
        Class: TasksGetViewSet
        Desc: Getting list of all tasks
        """

        url = reverse('tasks')
        response = self.client.get(url, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(resp_obj), 2)  # Counting total items

    def test_tasks_post_view(self):
        """
        Class: TasksPostViewSet
        Desc: Creating a new task
        """

        data = {'task_name': 'Meeting with team',
                'description': 'Practise presentation',
                'task_status': 'Not Started',
                'start_date': '2021-04-12',
                'deadline': '2021-04-12'}
        url = reverse('create-task')
        response = self.client.post(url, data, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 201)
        self.assertEquals(resp_obj, {'success': 'New Task Created'})

    def test_tasks_post_view_deadline(self):
        """
        Class: TasksPostViewSet
        Desc: 400 Error - End date should be >= than start date
        """

        data = {'task_name': 'Meeting with team',
                'description': 'Practise presentation',
                'task_status': 'Not Started',
                'start_date': '2021-04-12',
                'deadline': '2021-03-12'}
        url = reverse('create-task')
        response = self.client.post(url, data, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 400)
        self.assertEquals(resp_obj, {'detail': 'Invalid End Date'})

    def test_tasks_put_view(self):
        """
        Class: TasksPutViewSet
        Desc: Editing/ Updating a task
        """

        data = {'task_name': self.task_1.task_name,
                'description': 'Draw different shapes and color pattern',
                'start_date': self.task_1.start_date,
                'deadline': self.task_1.deadline,
                'task_status': self.task_1.task_status}
        url = reverse('edit-task', args=[self.task_1.id])
        response = self.client.put(url, data, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(resp_obj, {'success': ''})

    def test_tasks_put_view_deadline(self):
        """
        Class: TasksPutViewSet
        Desc: 400 Error - End date should be >= than start date
        """

        data = {'task_name': self.task_1.task_name,
                'description': 'Draw different shapes and color pattern',
                'start_date': self.task_1.start_date,
                'deadline': '2021-02-14',
                'task_status': self.task_1.task_status}
        url = reverse('edit-task', args=[self.task_1.id])
        response = self.client.put(url, data, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 400)
        self.assertEquals(resp_obj, {'detail': 'Invalid End Date'})

    def test_tasks_delete_view(self):
        """
        Class: TasksDeleteViewSet
        Desc: Deleting a task
        """

        # Checking if its deleted
        url = reverse('delete-task', args=[self.task_1.id])
        response = self.client.delete(url, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(resp_obj, {'success': ''})

        # Checking if the deleted task exists
        url = reverse('tasks')
        response = self.client.get(url, format='json')
        resp_obj = json.loads(str(response.content, 'utf-8'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(resp_obj), 1)  # Only one task should exist
        self.assertNotEqual(resp_obj[0]['id'], 1)  # ID should not match 1
