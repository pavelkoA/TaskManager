from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User
from task_manager.statuses.models import Status
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _


class TestStatusesWithoutAuth(TestCase):

    def setUp(self):
        self.login = reverse('login')
        self.urls = [reverse('statuses_list'),
                     reverse('status_create'),
                     reverse('status_delete', args=[1]),
                     reverse('status_update', args=[1])]

    def test_no_login(self):
        for u in self.urls:
            response = self.client.get(u)
            self.assertRedirects(response, self.login)


class StatusesTestCase(TestCase):
    fixtures = ['statuses.json', 'user.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)
        self.statuses = reverse('statuses_list')
        self.form_data = {'name': 'new status'}

    def test_status_list(self):
        self.first_status = Status.objects.get(pk=1)
        self.second_status = Status.objects.get(pk=5)
        self.third_status = Status.objects.get(pk=6)
        response = self.client.get(self.statuses)
        self.assertEqual(response.status_code, 200)
        response_tasks = list(response.context['statuses'])
        self.assertQuerysetEqual(response_tasks,
                                 [self.first_status, self.second_status,
                                  self.third_status])

    def test_create_status(self):
        self.create_status = reverse('status_create')

        get_response = self.client.get(self.create_status)
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(self.create_status,
                                         self.form_data, follow=True)
        self.assertRedirects(post_response, self.statuses)
        self.assertTrue(Status.objects.get(id=7))
        self.assertContains(
            post_response, text= _('Status successfully created'))

    def test_update_status(self):
        self.update_status = reverse('status_update', args=[1])

        get_response = self.client.get(self.update_status)
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(self.update_status,
                                         self.form_data, follow=True)
        self.assertRedirects(post_response, self.statuses)
        self.status = Status.objects.get(pk=1)
        self.assertEqual(self.status.name, self.form_data['name'])
        self.assertContains(
            post_response, text= _('Status successfully changed'))

    def test_delete_used_status(self):
        self.delete_status = reverse('status_delete', args=[1])

        get_response = self.client.get(self.delete_status)
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(self.delete_status)
        self.assertRedirects(post_response, self.statuses)
        self.assertEqual(len(Status.objects.all()), 2)

    def test_delete_not_used_status(self):
        self.delete_status = reverse('status_delete', args=[5])

        get_response = self.client.get(self.delete_status)
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(self.delete_status, follow=True)
        self.assertRedirects(post_response, self.statuses)
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(pk=5)
        self.assertContains(
            post_response, text= _('Status successfully delete'))