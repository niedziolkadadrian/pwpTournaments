from django.contrib import admin
from .models import Scoring, Tournament, Participant, Match

# Register your models here.
admin.site.register(Scoring)
admin.site.register(Tournament)
admin.site.register(Participant)
admin.site.register(Match)

