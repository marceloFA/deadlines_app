from django.db import models
from django.urls import reverse
from django.conf import settings
from users.models import Student
from multiselectfield import MultiSelectField


class ModelWithTimeStamp(models.Model):
    ''' safely adds create_at field to any model that inherits this '''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Task(ModelWithTimeStamp):
    ''' The Task model saves informations about a task, including its deadline '''
    # every value is a tuple (actual_value, human_redable_value)
    QUALIS_CHOICES = (
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('C1', 'C1'),
        ('C2', 'C2'),
        ('C3', 'C3'),
        ('C4', 'C4'),
        ('C5', 'C5'),
        ('', 'Does not apply')
    )

    event = models.CharField(max_length=200)
    event_url = models.CharField(max_length=500, null=True, blank=True)
    qualis = models.CharField(max_length=10, choices=QUALIS_CHOICES)
    deadline = models.DateField()
    students = models.ManyToManyField(Student, blank=True)
    
    def __str__(self):
        '''Console representation of a Task'''
        return self.event

    def get_absolute_url(self):
        return reverse('task:task_edit', kwargs={'pk': self.pk})
