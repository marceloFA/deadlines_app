from django import forms
from submissions.models import Submission
from events.models import Event
from users.models import Student


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = "__all__"

    def __init__(self, event_id, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.fields['event'].queryset = Event.objects.filter(id=event_id)

    # Students associated with this submission
    students = forms.ModelMultipleChoiceField(
        label='Select the students associated with this submission',
        queryset=Student.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
    )


    # The event that got a submission
    event = forms.ModelChoiceField(
        label='What event is associated with this submission?',
        queryset=None # defined by the __init__ method
        )

    # Submission status 
    status = forms.CharField(
        label="Submission status", widget=forms.Select(choices=Submission.STATUS_CHOICES)
    )

    # Paper url
    paper_url = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'special'}))

    # Paper Title
    paper_title = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'special'}))

    # Progress Percentage
    progress_percentage =  forms.IntegerField(widget=forms.NumberInput(attrs={'min':0,'max':100,'type':'range', 'step':5}))