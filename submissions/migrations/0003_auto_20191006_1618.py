# Generated by Django 2.2.5 on 2019-10-06 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0002_auto_20191006_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='event',
        ),
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(choices=[('1', 'Not yet defined'), ('2', 'Under Revision'), ('3', 'Accepted'), ('4', 'Rejected')], default='1', max_length=2),
        ),
    ]