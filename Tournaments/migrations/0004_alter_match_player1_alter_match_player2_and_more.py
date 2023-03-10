# Generated by Django 4.1.4 on 2023-01-21 10:19

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Tournaments', '0003_alter_tournament_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='player1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='player1', to='Tournaments.participant'),
        ),
        migrations.AlterField(
            model_name='match',
            name='player2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='player2', to='Tournaments.participant'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 21, 11, 19, 53, 226294)),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Organizer',
        ),
    ]
