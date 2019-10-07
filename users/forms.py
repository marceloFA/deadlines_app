from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Student


class StudentCreationForm(UserCreationForm):
    """ Custom form to create an student """

    class Meta:
        model = Student
        fields = ("name", "username")

    name = forms.CharField(
        label="Student Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Fill first and last name here",
            }
        ),
    )

    def clean(self): 
        name = self.cleaned_data.get('name') 
        username = self.cleaned_data.get('username') 

        if len(str(name).split(" ")) != 2:  
            self.add_error('name', 'Fill only first and last name here')
        return self.cleaned_data 


class StudentChangeForm(UserChangeForm):
    """ Custom form to change an student"""

    class Meta:
        model = Student
        fields = ("name", "username")

    name = forms.CharField(
        label="Student Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Fill first and last name here",
            }
        ),
    )


class AccountDeactivationForm(forms.Form):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "id": "password",
                "class": "form-control",
                "placeholder": "Password",
            }
        ),
    )


class ReactivationForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "id": "username",
                "class": "form-control",
                "placeholder": "Username",
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "id": "password",
                "class": "form-control",
                "placeholder": "Password",
            }
        ),
    )