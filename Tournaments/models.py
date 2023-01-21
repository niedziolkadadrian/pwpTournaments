import datetime

from django.db import models
from django.contrib.auth.models import User


class Scoring(models.Model):
    name = models.CharField(max_length=255)
    win_score = models.IntegerField()
    tie_score = models.IntegerField()
    loose_score = models.IntegerField()

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=datetime.datetime.now())
    confirmed = models.BooleanField(default=False)
    rules = models.ForeignKey(Scoring, on_delete=models.DO_NOTHING, blank=True, default=1, null=False)

    def __str__(self):
        return self.name


class Participant(models.Model):
    name = models.CharField(max_length=255)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player1 = models.ForeignKey(Participant, on_delete=models.DO_NOTHING, related_name='player1')
    player2 = models.ForeignKey(Participant, on_delete=models.DO_NOTHING, related_name='player2')
    player1_score = models.IntegerField()
    player2_score = models.IntegerField()
    date = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return str(self.player1) + " vs " + str(self.player2)
