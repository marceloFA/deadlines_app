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
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple
        )


class UpdateTaskForm(TaskForm):

    def __init__(self,task,*args,**kwargs):
        super (TaskForm,self ).__init__(*args,**kwargs) # populates the Task
        self.fields['students'].queryset = task.students.all()

    class Meta:
        model = Task
        fields = '__all__'