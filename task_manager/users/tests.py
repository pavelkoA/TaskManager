from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _


class UserTestCase(TestCase):
    fixtures = ['user.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.users_list = reverse('users_list')
        self.login = reverse('login')
        self.form_data = {'username': 'anotherUser',
                          'last_name': 'Another',
                          'first_name': 'User',
                          'password1': 'qwerty123!',
                          'password2': 'qwerty123!'}

    def test_users_list(self):
        response = self.client.get(self.users_list)
        self.assertEqual(response.status_code, 200)
        response_tasks = list(response.context['users'])
        self.assertQuerysetEqual(response_tasks,
                                 [self.user1, self.user2])

    def test_create_user(self):
        create_user = reverse('user_create')

        get_response = self.client.get(create_user)
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(create_user,
                                         self.form_data, follow=True)
        self.assertRedirects(post_response, self.login)
        self.assertTrue(User.objects.get(id=3))
        self.assertContains(post_response,
                            text=_('User successfully registered'))

    def test_update_user(self):
        self.client.force_login(self.user2)
        update_user = reverse('user_update', args=[2])

        get_response = self.client.get(update_user)
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(update_user,
                                         self.form_data, follow=True)
        self.assertRedirects(post_response, self.users_list)
        updated_user = User.objects.get(pk=2)
        self.assertEqual(updated_user.username, 'anotherUser')
        self.assertContains(post_response,
                            text=_('User successfully updated'))

    def test_update_user_no_permission(self):
        self.client.force_login(self.user2)
        updated_user = reverse('user_update', args=[1])

        get_response = self.client.get(updated_user,
                                       follow=True)
        self.assertRedirects(get_response, self.users_list)

        post_response = self.client.post(updated_user,
                                         self.form_data, follow=True)
        user = User.objects.get(id=1)
        self.assertRedirects(post_response, self.users_list)
        self.assertFalse(user.username == self.form_data['username'])

    def delete_user_no_permission(self):
        self.client.force_login(self.user3)
        del_user1 = reverse('delete', args=[1])

        get_response = self.client.get(del_user1)
        self.assertRedirects(get_response, self.users_list)
        self.assertEqual(len(User.objects.all()), 3)

        post_response = self.client.post(del_user1, follow=True)
        self.assertContains(post_response,
                            text=_("You have no rights to changed user."))

    def delete_user_without_tasks(self):
        self.client.force_login(self.user3)
        user = reverse('user_delete', args=[2])

        get_response = self.client.get(user, follow=True)
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(user, follow=True)
        self.assertRedirects(post_response, self.users_list)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(pk=3)
        self.assertContains(post_response,
                            text=_("User successfully deleted"))

    def delete_user_with_tasks(self):
        self.client.force_login(self.user1)
        user = reverse('user_delete', args=[1])

        get_response = self.client.get(user, follow=True)
        self.assertRedirects(get_response, self.users_list)
        self.assertEqual(len(User.objects.all()), 3)

        post_response = self.client.post(user, follow=True)
        self.assertContains(post_response,
                            text=_("You have no rights to deleted user."))
