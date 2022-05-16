import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from .models import Project


class ProjectSerializerTest(APITestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.get(pk=5)
        self.user_url = 'http://testserver' + reverse('employee-detail',
                                                      kwargs={'pk': self.user.pk})
        self.planned_date = timezone.now() + timezone.timedelta(days=7)
        prj = Project.objects.create(
            pk=1,
            manager=self.user,
            name='test name',
            description='test description',
            priority='High',
            planned_date=self.planned_date
        )

    def test_project_model(self):
        prj = Project.objects.get(pk=1)
        self.assertEqual(prj.name, 'test name')
        self.assertEqual(prj.status, 'In work')
        self.assertEqual(prj.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                         timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(prj.tasks.count(), 0)

    def test_project_view_list(self):

        resp = self.client.get('/task/projects/')
        data = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'test name')

    def test_project_create_from_view_good_request(self):
        response = self.client.post(
            '/task/projects/', {
                'manager': self.user_url,
                'name': 'test name 2',
                'description': 'test description 2',
                'priority': 'High',
                'planned_date': self.planned_date,
            }
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
        print('DATA CONTENT', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['name'], ['This field is required.'])

