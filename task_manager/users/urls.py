from django.urls import path, include
from task_manager.users import views


urlpatterns = (
    path('', views.users, name='users'),
    path('create/', views.user_create, name='user_create'),
)