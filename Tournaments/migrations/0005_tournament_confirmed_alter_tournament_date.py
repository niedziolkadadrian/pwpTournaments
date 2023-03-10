# Generated by Django 4.1.4 on 2023-01-21 12:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tournaments', '0004_alter_match_player1_alter_match_player2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 21, 13, 12, 37, 195707)),
        ),
    ]
