# Generated by Django 4.1.4 on 2023-01-21 13:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tournaments', '0007_scoring_name_alter_tournament_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 21, 14, 2, 41, 433517)),
        ),
    ]