from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('home')
    form_class = AuthenticationForm
    success_message = _('You are logged in')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)
