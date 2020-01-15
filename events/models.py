from django.db import models
from apps.models import ModelWithTimeStamp
from django.urls import reverse
from django.conf import settings
from users.models import Student

class Event(ModelWithTimeStamp):
    """ The Event model saves informations about a event, including its deadline """

    # every value is a tuple (actual_value, human_redable_value)
    QUALIS_CHOICES = (
        ("A1", "A1"),
        ("A2", "A2"),
        ("A3", "A3"),
        ("A4", "A4"),
        ("B1", "B1"),
        ("B2", "B2"),
        ("B3", "B3"),
        ("B4", "B4"),
        ("C", "C"),
        ("", "Does not apply"),
    )

    TYPE_CHOICES = (
        ("1", "Periodic"),
        ("2", "National Conference"),
        ("3", "International Conference"),
        ("4", "Journal"),
        ("4", "Workshops"),
        ("5", "Seminars"),
        ("6", "Others")
    )

    name = models.CharField(max_length=200)
    url = models.CharField(max_length=500, null=True, blank=True)
    qualis = models.CharField(max_length=10, choices=QUALIS_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True, blank=True)
    deadline = models.DateField()
    

    def __str__(self):
        """Console representation of a Event"""
        return self.name

    def get_absolute_url(self):
        return reverse("event:event_edit", kwargs={"pk": self.pk})