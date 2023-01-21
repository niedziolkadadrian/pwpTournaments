from django.shortcuts import render, HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Tournament, Match


# Create your views here.
class TournamentListView(ListView):
    model = Tournament
    template_name = "Tournaments/tournaments.html"


class TournamentDetailView(DetailView):
    model = Tournament
    template_name = "Tournaments/tournament.html"


class MatchDetailView(DetailView):
    model = Match
    template_name = "Tournaments/match.html"


def tournament_detail(request, id=1):
    return HttpResponse(str(id) + "TTTTTT")
