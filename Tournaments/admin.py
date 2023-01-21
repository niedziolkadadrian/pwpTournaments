from django.contrib import admin
from .models import Organizer, Tournament, Participant, Match

# Register your models here.
admin.site.register(Organizer)
admin.site.register(Tournament)
admin.site.register(Participant)
admin.site.register(Match)

