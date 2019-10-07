from django import forms
from submissions.models import Submission
from tasks.models import Task
from users.models import Student


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = "__all__"
        exclude = ('event',)

    # The task that got submitted
    task = forms.ModelChoiceField(
        label='What task is associated with this submission (Neither is an option)',
        queryset=Task.objects.all()
        )

    # Students associated with this submission
    students = forms.ModelMultipleChoiceField(
        label='Select the students associated with this submission',
        queryset=Student.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
    )

    # Submission status 
    status = forms.CharField(
        label="Submission status", widget=forms.Select(choices=Submission.STATUS_CHOICES)
    )