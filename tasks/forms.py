from django import forms
from tasks.models import Task
from users.models import Student
from bootstrap_datepicker_plus import DatePickerInput


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = '__all__'

    event = forms.CharField(
        label='Event Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Event Name'
        })
    )

    qualis = forms.CharField(
        label='Qualis',
        widget=forms.Select(choices=Task.QUALIS_CHOICES)
    )

    deadline = forms.DateField(
        required=True,
        label='deadline',
        widget=DatePickerInput(format='%Y-%m-%d')
    )

    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple
    )
