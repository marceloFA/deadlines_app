# Generated by Django 2.2.6 on 2019-10-24 12:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('submissions', '0005_auto_20191023_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='first_author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='papers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='submission',
            name='students',
            field=models.ManyToManyField(related_name='submissions', to=settings.AUTH_USER_MODEL),
        ),
    ]
