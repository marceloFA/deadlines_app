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

    paper_acronym = models.CharField(max_length=100, blank=False) 

    paper_url = models.CharField(max_length=400, blank=True, null=True)

    presentation_url = models.CharField(max_length=400, blank=True, null=True)

    rebuttal_url = models.CharField(max_length=400, blank=True, null=True)

    # Checklist fields ( related to the progress bar )
    implementation_done = models.BooleanField(blank=False, default=False)
    paper_introduction_done = models.BooleanField(blank=False, default=False)
    paper_related_works_done = models.BooleanField(blank=False, default=False)
    paper_proposal_done = models.BooleanField(blank=False, default=False)
    paper_results_done = models.BooleanField(blank=False, default=False)
    paper_figures_done = models.BooleanField(blank=False, default=False)
    paper_professors_revision_done = models.BooleanField(blank=False, default=False)
    