from django.contrib.auth import get_user_model
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.users.forms import UserForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import LoginRequiredAndUserSelfCheckMixin


class UsersView(ListView):
    template_name = 'users/users_list.html'
    model = get_user_model()
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'users/create.html'
    model = get_user_model()
    form_class = UserForm
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')


class UserUpdateView(LoginRequiredAndUserSelfCheckMixin,
                     SuccessMessageMixin,
                     UpdateView):
    template_name = 'users/update.html'
    model = get_user_model()
    form_class = UserForm
    success_url = reverse_lazy('users_list')
    success_message = _('User successfully updated')
    permission_message = _('You have no rights to changed user.')
    permission_url = reverse_lazy('users_list')


class UserDeleteView(LoginRequiredAndUserSelfCheckMixin,
                     SuccessMessageMixin,
                     DeleteView):
    template_name = 'users/delete.html'
    model = get_user_model()
    success_url = reverse_lazy('users_list')
    success_message = _('User successfully deleted')
    permission_message = _('You have no rights to deleted user.')
    permission_url = reverse_lazy('users_list')
