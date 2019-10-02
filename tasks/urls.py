from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
  path('', views.task_list, name='task_list'),
  path('<int:pk>',views.task_detail, name="task_detail"),
  path('new', views.task_create, name='task_new'),
  path('edit/<int:pk>', views.task_update, name='task_update'),
  path('delete/<int:pk>', views.task_delete, name='task_delete'),
] 