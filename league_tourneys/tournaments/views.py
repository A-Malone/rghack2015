import pprint
import json
import random

from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from models import Tournament, Match, Notification, Team, Summoner

from .forms import TournamentForm, TeamForm

from lib import challonge_api


def index(request):
    return render_to_response('index.html')

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
            
            short_code = data['shortCode']
            match = Match.objects.get(tournament_api_match_id=short_code)

            teams = match.teams.all()

            winning_player = data["winningTeam"][0]["summonerId"]
            if(winning_player in map(lambda x: x.summoner_id, teams[0].summoners.all())):
                winning_team = teams[0]
                losing_team = teams[1]
            else:                
                winning_team = teams[1]
                losing_team = teams[0]

            challonge_match_id = match.challonge_match_id
            swap = winning_team.pk != match.first_team_id
            match_results = {"scores_csv":"1-0" if swap else "0-1", "winner_id": winning_team.challonge_team_id}
            challonge_api.update_match(match.tournament.challonge_tournament_id, match.challonge_match_id, match_results)

            # Update the rest of the matches
            match.tournament.update_available_matches()

        pprint.pprint(data)
        return HttpResponse('Post json: ' + pprint.pformat(data))
    return HttpResponse('only POST requests pls rito')

# TOURNAMENT CONTROLLER
def tournament_detail_view(request, tournament_id):
    tournament = Tournament.objects.get(pk=int(tournament_id))

    match_map = {}
    for match in tournament.match_set.all():
        match_map[match.challonge_match_id] = match.pk

    return render(request, "tournament/detail.html", {"tournament": tournament, "match_map":match_map})

def start_tournament(request, tournament_id):
    tournament = Tournament.objects.get(pk=int(tournament_id))
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        tournament.start()        
    
    return redirect('tournament', tournament_id=tournament_id)

@login_required
def create_tournament(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = TournamentForm(request.POST)
        # check whether it"s valid:
        if form.is_valid():
            tournament = Tournament(name=form.cleaned_data["name"])
            form.cleaned_data['url'] = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
            tournament.setup(form.cleaned_data)
            tournament.save()
            return render(request, "tournament/detail.html", {"tournament": tournament})
    else:
        form = TournamentForm()
    return render(request, "tournament/create.html", {"form": form, "action":reverse("create_tournament")})


# MATCH CONTROLLER
def match_detail_view(request, tournament_id, match_id):
    tournament = Tournament.objects.get(pk=int(tournament_id))
    match = tournament.match_set.filter(pk=int(match_id)).first()

    teams = match.teams.all()   

    context = {'match':match, 'team1':teams.first(),'team2':teams.last(), 'players1':teams.first().summoners.all(), 'players2':teams.last().summoners.all()}
    return render(request, "match/detail.html", context)
 

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
                        
            return redirect('tournament', tournament_id=tournament_id)
    
    else:
        form = TeamForm()
    return render(request, "team/create.html", {"form": form, "action":reverse("create_team", args=[tournament.id])})
