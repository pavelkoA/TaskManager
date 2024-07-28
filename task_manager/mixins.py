from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


class CustomLoginRequiredMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        messages.error(self.request, _('Please log in.'))
        return redirect(reverse_lazy('login'))


class LoginRequiredAndUserSelfCheckMixin(CustomLoginRequiredMixin,
                                         UserPassesTestMixin):

    permission_message = ''
    permission_url = ''

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        else:
            messages.error(self.request, self.permission_message)
            return redirect(self.permission_url)


class UserPermissionMixin(UserPassesTestMixin):

    permission_message = ''
    permission_url = ''

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class AuthorPermissionMixin(UserPassesTestMixin):
    author_permission_message = ''
    author_permission_url = ''

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.author_permission_message)
        return redirect(self.author_permission_url)


class DeleteProtectionMixin:

    protected_message = ''
    protected_url = ''

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)
