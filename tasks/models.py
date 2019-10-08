from django.db import models
from apps.models import ModelWithTimeStamp
from django.urls import reverse
from django.conf import settings
from users.models import Student
from multiselectfield import MultiSelectField
from datetime import datetime

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
        """ Console representation of a Task object """
        return self.event

    def get_absolute_url(self):
        return reverse('task:task_edit', kwargs={'pk': self.pk})

    @property
    def progress_percentage(task):
        """ Returns the percentage based on the subtasks completed, and also based on the deadline """

        subtasks = SubTask.objects.all().filter(task = task)
        total_subtasks , completed_subtasks = len(subtasks) , 0
        for subtask in subtasks:
            if subtask.is_done:
                completed_subtasks+=1
        
        if (task.deadline - datetime.now().date()).days < 0 or task.is_done:
            progress_percentage = 100
        elif total_subtasks == 0:
            progress_percentage = 0
        else:
            progress_percentage = int((completed_subtasks/total_subtasks)*100)
        return progress_percentage

    @property
    def progress_background(self):
        """ Assigns a color for completion badge, from green to teal """
        percentage = self.progress_percentage
        if percentage == 100:
            badge_color = "bg-info"
        elif percentage >= 90:
            badge_color = "bg-danger"
        elif percentage >= 70:
            badge_color = "bg-warning"
        else:
            badge_color = "bg-success"
        return badge_color    

class SubTask(models.Model):
    """ This model represents a subtask of a task """
    name = models.CharField(max_length=100)
    is_done = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        """ Console representation of a SubTask object """
        return str([self.name, self.is_done])

