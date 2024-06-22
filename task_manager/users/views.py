from django.shortcuts import render
from django.http import HttpResponse

def users(request):
    return HttpResponse('All users')


def user_create(request):
    return HttpResponse('new users')
