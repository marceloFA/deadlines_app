from django import forms
from submissions.models import Submission
from events.models import Event
from users.models import Student


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = "__all__"

    # The event that got a submission
    event = forms.ModelChoiceField(
        label="What event is associated with this submission (Neither is an option)",
        queryset=Event.objects.all(),
    )

    # Students associated with this submission
    students = forms.ModelMultipleChoiceField(
        label="Select the students associated with this submission",
        queryset=Student.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
    )

    # Submission status
    status = forms.CharField(
        label="Submission status",
        widget=forms.Select(choices=Submission.STATUS_CHOICES),
    )

    # Paper url
    paper_url = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "special"})
    )
