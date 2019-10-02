from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
# Csutom User imports
from users.forms import StudentCreationForm, StudentChangeForm
from users.models import Student

# Register your models here.
class StudentAdmin(UserAdmin):
    add_form = StudentCreationForm
    form = StudentChangeForm
    model = Student
    list_display = ['name',]

admin.site.register(Student, StudentAdmin)

