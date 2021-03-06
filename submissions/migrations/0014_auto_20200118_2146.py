# Generated by Django 2.2.8 on 2020-01-18 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0013_auto_20200118_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='implementation_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='submission',
            name='paper_figures_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='submission',
            name='paper_introduction_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='submission',
            name='paper_professors_revision_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='submission',
            name='paper_proposal_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='submission',
            name='paper_related_works_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='submission',
            name='paper_reusults_done',
            field=models.BooleanField(default=False),
        ),
    ]
