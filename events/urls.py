from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("<int:pk>", views.event_detail, name="event_detail"),
    path("new", views.event_create, name="event_new"),
    path("edit/<int:pk>", views.event_update, name="event_update"),
    path("delete/<int:pk>", views.event_delete, name="event_delete"),
]
