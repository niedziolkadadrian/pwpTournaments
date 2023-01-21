from django.forms import ModelForm, HiddenInput
from .models import Participant


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
