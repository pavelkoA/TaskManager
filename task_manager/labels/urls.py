from django.urls import path
from task_manager.labels import views

urlpatterns = [
    path('', views.LabelListView.as_view(), name='labels'),
    path('create/', views.LabelAddView.as_view(), name='label_add'),
    path('<int:pk>/update/', views.LabelUpdateView.as_view(), name='label_update'),
    path('<int:pk>/delete/', views.LabelDeleteView.as_view(), name='label_delete'),
]