from django.contrib.auth import get_user_model
from django.views.generic import ListView

class UsersView(ListView):
    template_name = 'users/users_list.html'
    model = get_user_model()
    context_object_name = 'users'
