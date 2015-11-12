import pprint
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse

from models import Tournament, Match, Notification, Team

from .forms import TournamentForm, TeamForm


# Create your views here.
def index(request):
    return HttpResponse("hello rghack2015")

@csrf_exempt
def notification(request):
    ''' handle the POSTs that come from rito '''
    if request.method == 'POST':
        data = json.loads(request.body)
    print data
    pprint.pprint(request.POST.keys())
    Notification.objects.create(json_text=request.body)
    print Notification.objects.all()
    return HttpResponse('post json: ' + pprint.pformat(data))


# TOURNAMENT CONTROLLER
class TournamentDetailView(generic.DetailView):
    model = Tournament
    template_name = "tournament/detail.html"

def create_tournament(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = TournamentForm(request.POST)
        # check whether it"s valid:
        if form.is_valid():
            
            tournament = Tournament(name=form.cleaned_data["name"])            
            tournament.setup(dat)
            tournament.save()
            return render(request, "tournament/detail.html", {"tournament": tournament})
    
    else:
        form = TournamentForm()
    return render(request, "tournament/create.html", {"form": form, "action":reverse("create_tournament")})

# MATCH CONTROLLER
class MatchDetailView(generic.DetailView):
    model = Match
    template_name = "match/detail.html"

# TEAMS CONTROLLER
def create_team(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = TeamForm(request.POST)
        # check whether it"s valid:
        if form.is_valid():
            team = Team(name=form.cleaned_data["name"])

            participant = {}
            participant["name"] = team.name
            participant["misc"] = team.id
            p = challonge_api.create_participant(tournament.challonge_tournament_id, participant)

            team.challonge_team_id = p["participant"]["id"]
            
            for player_name in form.cleaned_data["members"]:
                summoner = Summoner.objects.get_or_create(summoner_name=player_name)
                team.summoners.add(summoner)

            tournament.teams.add(team)
                        
            return render(request, "team/detail.html", {"team": team})
    
    else:
        form = TeamForm()
    return render(request, "team/create.html", {"form": form, "action":reverse("create_team", args=[tournament.id])})