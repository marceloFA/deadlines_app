# Generated by Django 2.2.6 on 2019-10-24 00:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_event_progress_percentage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='is_done',
        ),
        migrations.RemoveField(
            model_name='event',
            name='progress_percentage',
        ),
        migrations.RemoveField(
            model_name='event',
            name='students',
        ),
    ]
