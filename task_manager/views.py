from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(LoginView):
    template_name = 'registration/login.html'


# class UserLogoutView(LogoutView):
#    next_page = reverse_lazy('index.html')