from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User
from task_manager.tasks.models import Task
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _


class TestTasksNotAuth(TestCase):

    def setUp(self):
        self.login = reverse('login')
        self.urls = [reverse('tasks_list'),
                     reverse('task_show', args=[1]),
                     reverse('task_create'),
                     reverse('task_delete', args=[1]),
                     reverse('task_update', args=[1])]

    def test_no_auth(self):
        for u in self.urls:
            response = self.client.get(u)
            self.assertRedirects(response, self.login)


class TasksTestCase(TestCase):
    fixtures = ['tasks.json', 'user.json',
                'statuses.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.tasks = reverse('tasks_list')
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        self.task3 = Task.objects.get(pk=3)
        self.delete_task = reverse('task_delete', args=[1])
        self.form_data = {'name': 'new task',
                          'status': 1,
                          'description': 'new description',
                          'executor': 1,
                          'label': [2]}

    def test_task_list(self):
        self.client.force_login(self.user)
        self.task = Task.objects.get(pk=1)

        response = self.client.get(self.tasks)
        self.assertEqual(response.status_code, 200)
        response_tasks = list(response.context['tasks'])
        self.assertQuerysetEqual(response_tasks,
                                 [self.task1,
                                  self.task2,
                                  self.task3])

    def test_show_task(self):
            self.client.force_login(self.user)
            self.show_task = reverse('task_show', args=[1])

            response = self.client.get(self.show_task)
            self.assertEqual(response.status_code, 200)
            descriptions = response.context['task']
            self.assertQuerysetEqual([descriptions.name,
                                      descriptions.author,
                                      descriptions.executor,
                                      descriptions.description,
                                      descriptions.status,
                                      descriptions.created_at],
                                     [self.task1.name, self.task1.author,
                                     self.task1.executor, self.task1.description,
                                     self.task1.status, self.task1.created_at])

    def test_create_task(self):
        self.client.force_login(self.user)
        self.create_task = reverse('task_create')

        get_response = self.client.get(self.create_task)
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(self.create_task,
                                         self.form_data,
                                         follow=True)
        self.assertRedirects(post_response, self.tasks)
        new_task = Task.objects.get(name=self.form_data['name'])
        self.assertEqual(new_task.executor.id, self.user.id)
        self.assertEqual(new_task.author.id, self.user.id)
        self.assertContains(post_response,
                            text=_('Task successfully created'))

    def test_update_task(self):
        self.client.force_login(self.user)
        self.update_task = reverse('task_update', args=[1])

        get_response = self.client.get(self.update_task)
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(self.update_task,
                                         self.form_data,
                                         follow=True)
        self.assertRedirects(post_response, self.tasks)
        self.assertEqual(Task.objects.get(pk=3).executor, self.user)
        self.assertContains(post_response,
                            text=_('Task successfully changed'))

    def test_delete_task(self):
        self.client.force_login(self.user)

        get_response = self.client.get(self.delete_task)
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(self.delete_task,
                                         follow=True)
        self.assertRedirects(post_response,self.tasks)
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(pk=4)
        self.assertContains(post_response,
                            text=_('Task successfully delete'))

def test_filter(self):
        self.client.force_login(self.user)

        content_type_form = f'{self.tasks}?status=1&executor=1&label='
        get_response = self.client.get(content_type_form)
        tasks_list = get_response.context['tasks']
        self.assertEqual(len(tasks_list), 1)
        task = tasks_list[0]
        self.assertEqual(task.name, 'Делишки')
        self.assertEqual(task.executor.id, 1)
        self.assertEqual(task.status.id, 1)

        content_type_form = f'{self.tasks}?status=3&executor=1&label='
        get_response = self.client.get(content_type_form)
        tasks_list = get_response.context['tasks']
        self.assertEqual(len(tasks_list), 1)
        task = tasks_list[0]
        self.assertEqual(task.name, 'Учеба')
        self.assertEqual(task.executor.id, 1)
        self.assertEqual(task.status.id, 1)