from django import forms
from events.models import Event
from users.models import Student
from bootstrap_datepicker_plus import DatePickerInput

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ("is_done", )

    name = forms.CharField(
        label="Event Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Event Name"}
        ),
    )

    url = forms.CharField(
        label="Event URL",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Event URL"}
        ),
    )

    qualis = forms.CharField(
        label="Qualis", widget=forms.Select(choices=Event.QUALIS_CHOICES)
    )

    deadline = forms.DateField(
        required=True, label="Deadline", widget=DatePickerInput(format="%Y-%m-%d")
    )

    progress_percentage =  forms.IntegerField(widget=forms.NumberInput(attrs={'min':0,'max':100,'type':'range', 'step':5}))

    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
    )

