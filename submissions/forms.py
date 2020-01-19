from django import forms
from submissions.models import Submission
from events.models import Event
from users.models import Student


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        exclude = ['event']
    
    # Students associated with this submission
    students = forms.ModelMultipleChoiceField(
        label='Select the students associated with this submission',
        queryset=Student.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    # Submission status 
    status = forms.CharField(
        label="Submission status", widget=forms.Select(choices=Submission.STATUS_CHOICES)
    )

    # Paper url
    paper_url = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'special'}))

    # Paper Acornym
    paper_acronym = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'special'}))



class EditSubmissionForm(SubmissionForm):
    class Meta:
        model = Submission
        fields = '__all__'
