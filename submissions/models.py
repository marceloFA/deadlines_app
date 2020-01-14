from django.db import models
from users.models import Student
from events.models import Event
from apps.models import ModelWithTimeStamp

class Submission(ModelWithTimeStamp):
    ''' This model stores informations about academic event submissions '''
    STATUS_CHOICES = (
        ('0', "In Writting Process"),
        ("1", "Not submitted"),
        ("2", "Under Revision"),
        ("3", "Accepted"),
        ("4", "Rejected"),
    )

    students = models.ManyToManyField(Student, blank=False, related_name='submissions')

    event = models.ForeignKey(Event, on_delete=models.SET_NULL,  null=True, related_name='submissions')

    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='0')

    paper_title = models.CharField(max_length=300, blank=True, null=True) 

    paper_url = models.CharField(max_length=300, blank=True, null=True)

    progress_percentage = models.IntegerField(default=0)