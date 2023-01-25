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
    def __init__(self, tournament, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields['player1'].queryset = Participant.objects.filter(tournament=tournament)
        self.fields['player2'].queryset = Participant.objects.filter(tournament=tournament)

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


class MatchScoreForm(ModelForm):
    class Meta:
        model = Match
        fields = ["player1_score", "player2_score"]
        labels = {
            "player1_score": "Wynik pierwszego uczestnika",
            "player2_score": "Wynik drugiego uczestnika",
        }


class ConfirmParticipantsForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ["confirmed"]
        widgets = {
            "confirmed": HiddenInput(),
        }
