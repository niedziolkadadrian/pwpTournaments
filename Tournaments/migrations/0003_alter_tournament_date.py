# Generated by Django 3.2.16 on 2023-01-19 10:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tournaments', '0002_auto_20230119_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 19, 11, 30, 4, 217982)),
        ),
    ]
