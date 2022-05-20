import json
from requests.auth import HTTPBasicAuth

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime, parse_time, parse_duration
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase, APITransactionTestCase

from .models import Project


class ProjectSerializerModelTest(APITestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.get(pk=5)
        self.user_url = 'http://testserver' + reverse('employee-detail',
                                                      kwargs={'pk': self.user.pk})
        self.planned_date = timezone.now() + timezone.timedelta(days=7)
        self.prj = Project.objects.create(
            pk=1,
            manager=self.user,
            name='test name',
            description='test description',
            priority='High',
            planned_date=self.planned_date
        )

    def test_project_model(self):
        self.assertEqual(self.prj.name, 'test name')
        self.assertEqual(self.prj.status, 'In work')
        self.assertEqual(self.prj.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                         timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(self.prj.tasks.count(), 0)

    def test_project_view_list(self):
        resp = self.client.get('/task/projects/')
        data = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'test name')

    def test_project_create_from_view_good_request(self):
        response = self.client.post(
            '/task/projects/', {
                'name': 'test name 2',
                'description': 'test description 2',
                'priority': 'High',
                'planned_date': self.planned_date,
            }, headers={'Authorization': 'Token 6009e1e66d8c5ef268b345091fe7d3c3794e49f1'}
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['name'], 'test name 2')
        self.assertEqual(data['status'], 'In work')

    def test_project_create_from_view_bad_request(self):
        response = self.client.post(
            '/task/projects/', {
                'manager': self.user_url,
            }
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['name'], ['This field is required.'])

    def test_calculation_time_project(self):
        url = reverse('project-detail', kwargs={'pk': self.prj.pk})
        response = self.client.put(
            url, {
                'manager': self.user_url,
                'name': 'test name 2',
                'description': 'test description 2',
                'priority': 'High',
                'planned_date': self.planned_date,
                'status': 'Finished'
            }
        )
