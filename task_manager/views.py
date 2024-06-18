from django.shortcuts import render
from django.utils.translation import gettext


def index(request):
    return render(request, 'task_manager/index.html')
