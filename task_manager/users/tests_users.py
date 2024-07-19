import os
import json
from django.test import TestCase
from django.urls import reverse_lazy
from task_manager.users.models import User


class UserTestCase(TestCase):
    fixtures = ['user.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fixture = os.path.join(
            os.path.dirname(__file__), os.path.pardir,
            'fixtures', 'user_data.json'
        )
        with open(fixture, 'r') as file:
            cls.user_data = json.load(file)

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)


class TestCreateUser(UserTestCase):

    def test_open_without_login(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('users_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_status(self):
        initial_count = User.objects.count()
        response = self.client.post(
            reverse_lazy('user_create'), self.user_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), initial_count + 1)

        new_user = User.objects.latest('id')
        self.assertEqual(new_user.username, self.user_data['username'])
        self.assertEqual(new_user.first_name, self.user_data['first_name'])
        self.assertEqual(new_user.last_name, self.user_data['last_name'])


class TestUpdateUser(UserTestCase):

    def test_update_without_login(self):
        self.client.logout()
        response = self.client.get(
            reverse_lazy(
                'user_update', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)

    def test_update_status(self):
        response = self.client.get(
            reverse_lazy('user_update', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse_lazy(
                'user_update', kwargs={'pk': 1}), self.user_data
        )
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(pk=1)
        self.assertEqual(updated_user.username, self.user_data['username'])
        self.assertEqual(updated_user.first_name, self.user_data['first_name'])
        self.assertEqual(updated_user.last_name, self.user_data['last_name'])


class TestDeleteUser(UserTestCase):

    def test_delete_without_login(self):
        self.client.logout()
        response = self.client.get(
            reverse_lazy('user_delete', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_status(self):
        initial_count = User.objects.count()
        response = self.client.post(
            reverse_lazy('user_delete', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), initial_count - 1)