from django.db import models
from users.models import Student
from events.models import Event
from apps.models import ModelWithTimeStamp

class Submission(ModelWithTimeStamp):
    ''' This model stores informations about academic event submissions '''
    STATUS_CHOICES = (
        ('0', "In Writting Process"),
        ("1", "Not yet defined"),
        ("2", "Under Revision"),
        ("3", "Accepted"),
        ("4", "Rejected"),
    )

    students = models.ManyToManyField(Student, blank=False)

    event = models.ForeignKey(Event, on_delete=models.SET_NULL,  null=True, related_name='event')

    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='0')

    paper_title = models.CharField(max_length=300, blank=True, null=True) 

    paper_url = models.CharField(max_length=300, blank=True, null=True)

    progress_percentage = models.IntegerField(default=0)

    submitted = models.BooleanField(default=False)



@property
def progress_color(self):
    """ Assigns a color for completion badge, from black at 0% to green at 100% """
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