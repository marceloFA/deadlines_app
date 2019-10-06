from django.db import models
from users.models import Student
from tasks.models import Task

# Create your models here.


class Submissions(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    tasks = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField()
    url = models.CharField(max_length=300)
