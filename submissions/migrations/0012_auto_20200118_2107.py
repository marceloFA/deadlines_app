# Generated by Django 2.2.8 on 2020-01-18 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0011_auto_20200114_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='paper_acronym',
            field=models.CharField(default='INSERT A NAME FOR THIS SUBMISSION', max_length=100),
        ),
    ]
