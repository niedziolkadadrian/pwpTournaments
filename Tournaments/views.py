import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Tournament, Match, Participant
from .forms import ParticipantForm, TournamentForm


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


@login_required(login_url="/admin/")
def add_tournament(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            t = form.save()
            return redirect(f'/tournament/{t.id}/')
    else:
        form = TournamentForm(initial={"date": datetime.datetime.now(), "organizer": request.user})
    context = {"form": form}
    return render(request, "Tournaments/tournament_add.html", context)


@login_required(login_url="/admin/")
def del_tournament(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    if request.user != tournament.organizer:
        messages.error(request, 'Nie możesz usunąć tego turnieju! Nie jesteś jego organizatorem.')
        return redirect("/myTournaments/")

    if request.method == 'POST':
        tournament.delete()
        messages.success(request, 'Pomyślnie usunięto turniej: '+str(tournament)+"!")
        return redirect("/myTournaments/")

    context = {"Tournament": tournament}
    return render(request, "Tournaments/tournament_del.html", context)


@login_required(login_url="/admin/")
def add_participant(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    if request.user != tournament.organizer or tournament.confirmed:
        messages.error(request, "Nie możesz usunąć uczestnika! Nie jesteś organizatorem tego turnieju.")
        return redirect(f"/tournament/{pk}/")
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return redirect(f'/tournament/{pk}/')
    else:
        form = ParticipantForm(initial={"tournament": pk})
    context = {"form": form, "pk": pk, "Tournament": tournament}
    return render(request, "Tournaments/participant_add.html", context)


@login_required(login_url="/admin/")
def del_participant(request, tournament_id, pk):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    participant = get_object_or_404(Participant, pk=pk)
    if request.user != tournament.organizer or tournament.confirmed:
        messages.error(request, "Nie możesz usunąć uczestnika! Nie jesteś organizatorem tego turnieju.")
        return redirect(f"/tournament/{pk}/")
    if request.method == 'POST':
        participant.delete()
        messages.success(request, "Pomyślnie usunięto uczestnika: "+str(participant)+"!")
        return redirect(f'/tournament/{tournament_id}/')
    context = {"Tournament": tournament, "participant": participant}
    return render(request, "Tournaments/participant_del.html", context)
