from django.urls import path

from . import views

app_name = "submissions"

urlpatterns = [
    path("", views.submission_list, name="submission_list"),
    path("<int:pk>", views.submission_detail, name="submission_detail"),
    path("new/<int:event_pk>", views.submission_create, name="submission_new"),
    path("edit/<int:pk>", views.submission_update, name="submission_update"),
    path("delete/<int:pk>", views.submission_delete, name="submission_delete"),
    path("done/<int:pk>", views.submission_done, name="submission_done"),
    path("undone/<int:pk>", views.submission_undone, name="submission_undone"),
]
