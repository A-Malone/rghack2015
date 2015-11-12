from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from models import Tournament, Match

# Create your views here.
def index(request):
    return HttpResponse("hello rghack2015")

class TournamentDetailView(generic.DetailView):
    model = Tournament
    template_name = 'tournament/detail.html'

class MatchDetailView(generic.DetailView):
    model = Match
    template_name = 'match/detail.html'
