from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User
from task_manager.labels.models import Label
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _


class TestLabelsNotAuth(TestCase):

    def setUp(self):
        self.login = reverse('login')
        self.urls = [reverse('labels_list'),
                     reverse('label_create'),
                     reverse('label_delete', args=[1]),
                     reverse('label_update', args=[1])]

    def test_no_login(self):
        for u in self.urls:
            response = self.client.get(u)
            self.assertRedirects(response, self.login)


class LabelsTestCase(TestCase):
    fixtures = ['labels.json', 'user.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)
        self.labels = reverse('labels_list')
        self.form_data = {'name': 'new label'}

    def test_labels_list(self):
        response = self.client.get(self.labels)
        self.assertEqual(response.status_code, 200)
        labels = list(response.context['labels'])
        self.assertEqual(len(labels), 3)
        self.assertEqual(labels[0].name, "Бросай все и делай")

    def test_create_label(self):
        self.create_label = reverse('label_create')

        get_response = self.client.get(self.create_label)
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(self.create_label,
                                         self.form_data,
                                         follow=True)
        self.assertRedirects(post_response, self.labels)
        new_label = Label.objects.get(name=self.form_data['name'])
        self.assertEqual(new_label.id, 4)
        self.assertContains(post_response,
                            text=_('Label successfully created'))

    def test_update_label(self):
        self.update_label = reverse('label_update', args=[1])

        get_response = self.client.get(self.update_label)
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(self.update_label,
                                         self.form_data,
                                         follow=True)
        self.assertRedirects(post_response, self.labels)
        updated_label = Label.objects.get(pk=1)
        self.assertEqual(updated_label.name, 'new label')
        self.assertContains(post_response,
                            text=_('Label successfully changed'))

    def test_delete_used_label(self):
        self.delete_label = reverse('label_delete', args=[1])

        get_response = self.client.get(self.delete_label,
                                       follow=True)
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(self.delete_label,
                                         follow=True)
        self.assertRedirects(post_response, self.labels)
        self.assertEqual(len(Label.objects.all()), 2)

    def test_delete_not_used_label(self):
        self.delete_label = reverse('label_delete', args=[2])

        get_response = self.client.get(self.delete_label,
                                       follow=True)
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(self.delete_label,
                                         follow=True)
        self.assertRedirects(post_response, self.labels)
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(pk=2)
        self.assertContains(post_response,
                            text=_('Label successfully delete'))
