# Generated by Django 2.2.6 on 2019-10-11 00:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="students",
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        )
    ]
