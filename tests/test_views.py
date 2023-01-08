from unittest import mock

import requests
from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from unittest.mock import Mock
from package.forms import PackageForm
from package.models import Package
from package.views import PackageListView
from rest_framework.test import APITestCase, APIRequestFactory, APIClient, RequestsClient
from rest_framework_simplejwt.tokens import RefreshToken
from ticket.models import Ticket, Department
from rest_framework import status
from ticket.serializers import TicketSerializer, TicketReadSerializer
from model_bakery import baker
import json
import datetime
from requests.exceptions import Timeout


class TestPackage(TestCase):
    def setUp(self):
        User.objects.create_user(username='saman', email='saman@gmail.com', password='123456')
        self.client = Client()
        self.client.login(username='saman', email='saman@gmail.com', password='123456')

    def test_package_list(self):
        response = self.client.get(reverse('package-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'package/list.html')

    def test_package_form_GET(self):
        response = self.client.get(reverse('package-form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'package/form.html')
        self.failUnless(response.context['form'], PackageForm)

    def test_package_form_POST(self):
        response = self.client.post(reverse('package-form'), data={
            'type': 1,
            'title': 'aaaaa',
            'machine_limit': 1,
            'pricing': 1,
            'per_second': 1,
            'priority': 1,
            'ghz': 1,
            'sort_order': 1,
            'is_unlimited': 1,
            'is_active': 1,
            'users': 1,
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('package-list'))
        self.assertEqual(Package.objects.count(), 1)

    def test_package_form_POST_invalid(self):
        response = self.client.post(reverse('package-form'), data={
            'type': 1,
            'title': 'aaa',
            'machine_limit': 1,
            'pricing': 1,
            'per_second': 1,
            'priority': 1,
            'ghz': 1,
            'sort_order': 1,
            'is_unlimited': 1,
            'is_active': 1,
            'users': 1,
        })
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response.context['form'], 'title', 'Length is < 5')


class TestPackageAuth(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='saman', email='saman@gmail.com', password='123456')
        self.factory = RequestFactory()

    def test_package_list_user_auth(self):
        request = self.factory.get(reverse('package-list'))
        request.user = self.user
        response = PackageListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_package_list_user_anonymous(self):
        request = self.factory.get(reverse('package-list'))
        request.user = AnonymousUser
        response = PackageListView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestTicket(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='saman', email='js@js.com', password='123456', is_superuser=True,
                                             is_staff=True)
        refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # create a ticket
        self.ticket = baker.make(Ticket)

        self.department = baker.make(Department)

    def test_list(self):
        response = self.client.get('/ticket/tickets/')
        tickets = Ticket.objects.all()
        serializer = TicketReadSerializer(tickets, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.data['count'], 1)

    def test_list_invalid_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer ')
        response = self.client.get('/ticket/tickets/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create(self):
        response = self.client.post(
            '/ticket/tickets/',
            data={
                "user": self.user.id,
                "department": self.department.id,
                "subject": "sub",
                "message": "mes",
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_no_data(self):
        response = self.client.post('/ticket/tickets/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_one(self):
        response = self.client.get("/ticket/tickets/{}/".format(self.ticket.id))
        ticket = Ticket.objects.get(pk=self.ticket.id)
        serializer = TicketReadSerializer(ticket)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_invalid(self):
        response = self.client.get("/ticket/tickets/{}/".format(1234))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


tuesday = datetime.datetime(year=2019, month=1, day=1)
sunday = datetime.datetime(year=2019, month=1, day=6)
datetime = Mock()
requests = Mock()


class TestMock(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='saman', email='js@js.com', password='123456', is_superuser=True,
                                             is_staff=True)
        refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # create a ticket
        self.ticket = baker.make(Ticket)

        self.department = baker.make(Department)

    def test_mock(self):
        datetime.datetime.today.return_value = tuesday
        today = datetime.datetime.today()
        self.assertIn(today.weekday(), [0, 1, 2, 3, 4, 5])

    @mock.patch('ticket.models.Ticket.save')
    def test_mock_side_effect(self, mock_save):
        mock_save.side_effect = Exception('db fail!!!')

        with self.assertRaises(Exception):
            response = self.client.post(
                '/ticket/tickets/',
                data={
                    "user": self.user.id,
                    "department": self.department.id,
                    "subject": "sub",
                    "message": "mes",
                }
            )

