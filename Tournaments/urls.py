"""pwpTournaments URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import *


urlpatterns = [
    path("", TournamentListView.as_view()),
    path("myTournaments/", organizer_tournaments_list),
    path("tournament/<pk>/", TournamentDetailView.as_view()),
    path("addTournament/", add_tournament),
    path("delTournament/<pk>/", del_tournament),

    path("tournament/<pk>/addParticipant/", add_participant),
    path("tournament/<tournament_id>/delParticipant/<pk>/", del_participant),
    path("tournament/<pk>/confirmParticipants/", confirm_participants),

    path("match/<pk>/", MatchDetailView.as_view()),
    path("tournament/<pk>/addMatch/", add_match),
    path("delMatch/<pk>/", del_match),
    path("match/<pk>/setScore/", upd_match),
]
