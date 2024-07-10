from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext
from .models import User


class UserForm(UserCreationForm):

    first_name = forms.CharField(max_length=250,
                                 required=True, label=gettext("First name"))
    last_name = forms.CharField(max_length=250,
                                required=True, label=gettext("Last name"))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'password1', 'password2')


class UpdateUserForm(UserForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username