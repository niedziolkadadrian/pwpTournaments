from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required

from .models import Tournament, Match, Participant
from .forms import ParticipantForm


# Create your views here.
class TournamentListView(ListView):
    model = Tournament
    template_name = "Tournaments/tournaments.html"
    extra_context = {"title": "Lista turnieji", "manage": False}


class TournamentDetailView(DetailView):
    model = Tournament
    template_name = "Tournaments/tournament.html"


class MatchDetailView(DetailView):
    model = Match
    template_name = "Tournaments/match.html"


@login_required(login_url="/admin/")
def organizer_tournaments_list(request):
    queryset = Tournament.objects.filter(organizer=request.user)
    context = {"object_list": queryset, "title": "Lista turnieji organizowanych przez ciebie.", "manage": True}
    return render(request, "Tournaments/tournaments.html", context=context)


def add_participant(request, pk):
    tournament = Tournament.objects.get(id=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        print(form.data.keys())
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return redirect(f'/tournament/{pk}/')
    else:
        form = ParticipantForm({"tournament": pk})
    context = {"form": form, "pk": pk, "Tournament": tournament}
    return render(request, "Tournaments/participant_add.html", context)
