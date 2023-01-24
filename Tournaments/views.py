import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Tournament, Match, Participant
from .forms import ParticipantForm, TournamentForm, MatchForm, MatchScoreForm, ConfirmParticipantsForm


# Create your views here.
class TournamentListView(ListView):
    model = Tournament
    template_name = "Tournaments/tournaments.html"
    queryset = Tournament.objects.all().order_by("-date")
    extra_context = {"title": "Lista turnieji", "manage": False}


class TournamentDetailView(DetailView):
    model = Tournament
    template_name = "Tournaments/tournament.html"


class MatchDetailView(DetailView):
    model = Match
    template_name = "Tournaments/match.html"


@login_required(login_url="login")
def organizer_tournaments_list(request):
    queryset = Tournament.objects.filter(organizer=request.user).order_by("-date")
    context = {"object_list": queryset, "title": "Lista turnieji organizowanych przez ciebie.", "manage": True}
    return render(request, "Tournaments/tournaments.html", context=context)


@login_required()
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


@login_required()
def del_tournament(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    if request.user != tournament.organizer:
        messages.error(request, 'Nie możesz usunąć tego turnieju! Nie jesteś jego organizatorem.')
        return redirect("my_tournaments")

    if request.method == 'POST':
        tournament.delete()
        messages.success(request, 'Pomyślnie usunięto turniej: ' + str(tournament) + "!")
        return redirect("my_tournaments")

    context = {"Tournament": tournament}
    return render(request, "Tournaments/tournament_del.html", context)


@login_required()
def confirm_participants(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    if request.user != tournament.organizer:
        messages.error(request, 'Nie możesz zatwierdzić uczestników turnieju! Nie jesteś jego organizatorem.')
        return redirect("my_tournaments")
    elif tournament.confirmed:
        messages.error(request, "Nie możesz zatwierdzić uczestników turnieju! Lista uczestników jest już zatwierdzona.")
        return redirect("tournament", pk=pk)

    if request.method == 'POST':
        form = ConfirmParticipantsForm(request.POST, instance=tournament)
        # check whether it's valid:
        if form.is_valid():
            t = form.save()
            messages.success(request, "Pomyślnie zatwierdzono listę uczestników turnieju: " + str(t) + "!")
            return redirect("tournament", pk=pk)
    else:
        form = ConfirmParticipantsForm(instance=tournament, initial={'confirmed': True})
    context = {"form": form, "Tournament": tournament}
    return render(request, "Tournaments/tournament_upd.html", context)


@login_required()
def add_participant(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    if request.user != tournament.organizer:
        messages.error(request, "Nie możesz dodać uczestnika! Nie jesteś organizatorem tego turnieju.")
        return redirect("tournament", pk=pk)
    elif tournament.confirmed:
        messages.error(request, "Nie możesz dodać uczestnika! Lista uczestników jest już zatwierdzona.")
        return redirect("tournament", pk=pk)

    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            u = form.save()
            messages.success(request, "Pomyślnie dodano uczestnika: " + str(u) + "!")
            return redirect("tournament", pk=pk)
    else:
        form = ParticipantForm(initial={"tournament": pk})
    context = {"form": form, "pk": pk, "Tournament": tournament}
    return render(request, "Tournaments/participant_add.html", context)


@login_required()
def del_participant(request, tournament_id, pk):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    participant = get_object_or_404(Participant, pk=pk)
    if request.user != tournament.organizer:
        messages.error(request, "Nie możesz usunąć uczestnika! Nie jesteś organizatorem tego turnieju.")
        return redirect("tournament", pk=tournament_id)
    elif tournament.confirmed:
        messages.error(request, "Nie możesz usunąć uczestnika! Lista uczestników jest już zatwierdzona.")
        return redirect("tournament", pk=tournament_id)

    if request.method == 'POST':
        participant.delete()
        messages.success(request, "Pomyślnie usunięto uczestnika: " + str(participant) + "!")
        return redirect("tournament", pk=tournament_id)
    context = {"Tournament": tournament, "participant": participant}
    return render(request, "Tournaments/participant_del.html", context)


@login_required()
def add_match(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    if request.user != tournament.organizer:
        messages.error(request, "Nie możesz dodać meczu! Nie jesteś organizatorem tego turnieju.")
        return redirect("tournament", pk=pk)
    elif not tournament.confirmed:
        messages.error(request, "Nie możesz dodać meczu! Lista uczestników nie jest jeszcze zatwierdzona.")
        return redirect("tournament", pk=pk)

    if request.method == 'POST':
        form = MatchForm(tournament, request.POST)
        # check whether it's valid:
        if form.is_valid():
            m = form.save()
            messages.success(request, "Pomyślnie dodano mecz: " + str(m) + "!")
            return redirect("tournament", pk=pk)
    else:
        form = MatchForm(tournament=tournament, initial={"date": datetime.datetime.now(), "tournament": pk})
    context = {"form": form, "pk": pk, "Tournament": tournament}
    return render(request, "Tournaments/match_add.html", context)


@login_required()
def del_match(request, pk):
    match = get_object_or_404(Match, pk=pk)
    tournament = match.tournament
    if request.user != tournament.organizer:
        messages.error(request, "Nie możesz usunąć meczu! Nie jesteś organizatorem tego turnieju.")
        return redirect("match", pk=pk)
    elif not tournament.confirmed:
        messages.error(request, "Nie możesz usunąć meczu! Lista uczestników nie jest jeszcze zatwierdzona.")
        return redirect("match", pk=pk)

    if request.method == 'POST':
        match.delete()
        messages.success(request, "Pomyślnie usunięto mecz: " + str(match) + "!")
        return redirect("tournament", pk=tournament.id)
    context = {"Tournament": tournament, "match": match}
    return render(request, "Tournaments/match_del.html", context)


@login_required()
def upd_match(request, pk):
    match = get_object_or_404(Match, pk=pk)
    tournament = match.tournament
    if request.user != tournament.organizer:
        messages.error(request, "Nie możesz zmienić wyniku meczu! Nie jesteś organizatorem tego turnieju.")
        return redirect("match", pk=pk)
    elif not tournament.confirmed:
        messages.error(request, "Nie możesz zmienić wyniku meczu! Lista uczestników nie jest jeszcze zatwierdzona.")
        return redirect("match", pk=pk)

    if request.method == 'POST':
        form = MatchScoreForm(request.POST, instance=match)
        # check whether it's valid:
        if form.is_valid():
            m = form.save()
            messages.success(request, "Pomyślnie zaktualizowano wynik meczu: " + str(m) +
                             " (" + str(m.player1_score) + ":" + str(m.player2_score) + ")!")
            return redirect("match", pk=pk)
    else:
        form = MatchScoreForm(instance=match)
    context = {"form": form, "pk": pk, "Tournament": tournament, "match": match}
    return render(request, "Tournaments/match_upd.html", context)


def get_participant_results(tournament, participant):
    results = []
    for match in tournament.match_set.all():
        if match.player1 == participant:
            result = "tie"
            if match.player1_score > match.player2_score:
                result = "win"
            elif match.player1_score < match.player2_score:
                result = "loose"
            results.append({"match": match, "result": result})
        elif match.player2 == participant:
            result = "tie"
            if match.player1_score > match.player2_score:
                result = "loose"
            elif match.player1_score < match.player2_score:
                result = "win"
            results.append({"match": match, "result": result})
    return results


def calculate_points(results, scoring):
    score = 0
    for result in results:
        if result["result"] == "win":
            score += scoring.win_score
        elif result["result"] == "tie":
            score += scoring.tie_score
        elif result["result"] == "loose":
            score += scoring.loose_score
    return score


def get_scoreboard(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    scoring = tournament.rules
    context = {"participants": []}
    for participant in tournament.participant_set.all():
        results = get_participant_results(tournament, participant)
        score = calculate_points(results, scoring)
        context["participants"].append({"participant": participant, "score": score, "results": results})

    context["participants"].sort(key=lambda pp: pp["score"], reverse=True)
    return render(request, "Tournaments/scoreboard.html", context)
