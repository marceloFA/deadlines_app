# Generated by Django 2.2.5 on 2019-10-02 00:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("tasks", "0009_task_students")]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="students",
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        )
    ]
