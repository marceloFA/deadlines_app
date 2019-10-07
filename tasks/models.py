from django.db import models
from apps.models import ModelWithTimeStamp
from django.urls import reverse
from django.conf import settings
from users.models import Student
from multiselectfield import MultiSelectField

class Task(ModelWithTimeStamp):
    """ The Task model saves informations about a task, including its deadline """

    # every value is a tuple (actual_value, human_redable_value)
    QUALIS_CHOICES = (
        ("A1", "A1"),
        ("A2", "A2"),
        ("B1", "B1"),
        ("B2", "B2"),
        ("C1", "C1"),
        ("C2", "C2"),
        ("C3", "C3"),
        ("C4", "C4"),
        ("C5", "C5"),
        ("", "Does not apply"),
    )

    STATUS_CHOICES = (
        ("1", "Enable"),
        ("2", "Canceled"),
        ("3", "Done"),
    )

    event = models.CharField(max_length=200)
    event_url = models.CharField(max_length=500, null=True, blank=True)
    qualis = models.CharField(max_length=10, choices=QUALIS_CHOICES)
    deadline = models.DateField()
    students = models.ManyToManyField(Student, blank=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        """Console representation of a Task"""
        return self.event

    def get_absolute_url(self):
        return reverse("task:task_edit", kwargs={"pk": self.pk})

    @property
    def get_progress_percentage(self):
        """ Return the percentage of time left for a certain task based on its deadline date """
        created_at_date = self.created_at.date()
        total_days = (self.deadline - created_at_date).days
        progress_percentage = (
            100 - (100 * self.days_left / total_days) if self.days_left > 0 else 100
        )
        return int(progress_percentage)

    @property
    def progress_color(self):
        """ Assigns a color for completion badge, from black at 0% to green at 100% """
        percentage = self.get_progress_percentage
        if percentage == 100:
            badge_color = "bg-info"
        elif percentage >= 90:
            badge_color = "bg-danger"
        elif percentage >= 70:
            badge_color = "bg-warning"
        else:
            badge_color = "bg-success"
        return badge_color