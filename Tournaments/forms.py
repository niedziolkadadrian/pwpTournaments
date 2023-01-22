from django.forms import ModelForm, HiddenInput, DateTimeInput
from .models import Participant, Tournament, Match


class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        fields = ["name", "tournament"]
        widgets = {
            "tournament": HiddenInput()
        }
        labels = {
            "name": "Nazwa uczestnika"
        }


class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ["name", "description", "date", "rules", "organizer"]
        widgets = {
            "organizer": HiddenInput(),
            "date": DateTimeInput(attrs={"type": "datetime-local"}),
        }
        labels = {
            "name": "Nazwa turnieju",
            "description": "Opis",
            "date": "Data turnieju",
            "rules": "Zasady punktowania (wygrana/remis/przegrana)",
        }


class MatchForm(ModelForm):
    class Meta:
        model = Match
        fields = ["player1", "player2", "date", "tournament"]
        widgets = {
            "tournament": HiddenInput(),
            "date": DateTimeInput(attrs={"type": "datetime-local"}),
        }
        labels = {
            "player1": "Pierwszy uczestnik",
            "player2": "Drugi uczestnik",
            "date": "Data meczu",
        }

