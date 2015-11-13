import pprint
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from models import Tournament, Match, Notification, Team, Summoner

from .forms import TournamentForm, TeamForm


def index(request):
    return HttpResponse('hello rghack2015')

def list(request):
    data = Tournament.objects.all()
    pprint.pprint(data)
    return render(request, "tournament/list.html", {"data": data})

@csrf_exempt
def notification(request):
    ''' handle the POSTs that come from rito '''
    if request.method == 'POST':
        data = json.loads(request.body)
        if 'shortCode' in data:
            Notification.objects.create(tournament_code=data['shortCode'],
                                        json_text=request.body)
        pprint.pprint(data)
        return HttpResponse('Post json: ' + pprint.pformat(data))
    return HttpResponse('only POST requests pls rito')


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
            tournament.setup(form.cleaned_data)
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
    tournament = Tournament.objects.get(pk=int(tournament_id))
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = TeamForm(request.POST)
        # check whether it"s valid:
        if form.is_valid():
            team = Team.create(form.cleaned_data["name"], tournament)

            for player_name in form.cleaned_data["members"].split(","):

                summoner = Summoner.find_or_create(player_name)
                team.summoners.add(summoner)
                        
            return render(request, "team/detail.html", {"team": team})
    
    else:
        form = TeamForm()
    return render(request, "team/create.html", {"form": form, "action":reverse("create_team", args=[tournament.id])})
