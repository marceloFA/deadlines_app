from django.contrib.auth.models import AbstractUser
from django.db import models

class Student(AbstractUser):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name