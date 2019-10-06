from django import forms
from tasks.models import Task, SubTask
from users.models import Student
from bootstrap_datepicker_plus import DatePickerInput


class TaskForm(forms.ModelForm):

    """ Form for editing or creating a Task object """

    class Meta:
        model = Task
        fields = "__all__"

    event = forms.CharField(
        label="Event Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Event Name"}
        ),
    )

    qualis = forms.CharField(
        label="Qualis", widget=forms.Select(choices=Task.QUALIS_CHOICES)
    )

    deadline = forms.DateField(
        required=True, label="deadline", widget=DatePickerInput(format="%Y-%m-%d")
    )

    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
    )

class SubTaskForm(forms.Form):
    """ Form to toggle created subtasks and to create a SubTask object """
    def __init__(self,*args,**kwargs):
        super().__init__()

        # task is the Task object passed to the form
        task = kwargs.pop('task')

        # The boolean fields for existing SubTask objects 
        for subtask in SubTask.objects.all().filter(task = task):
            self.fields[subtask.name] = forms.BooleanField(required = False, initial = subtask.is_done)
        
        # the 'add' field is for creating a SubTask object
        self.fields['add'] = forms.CharField(required=False,max_length=100,label='Add SubTask')