# Generated by Django 4.1.4 on 2023-01-25 18:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tournaments', '0010_auto_20230124_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
