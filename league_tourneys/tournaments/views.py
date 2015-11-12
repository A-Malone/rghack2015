import pprint
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from models import Tournament, Match, Notification

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

class TournamentDetailView(generic.DetailView):
    model = Tournament
    template_name = 'tournament/detail.html'

class MatchDetailView(generic.DetailView):
    model = Match
    template_name = 'match/detail.html'
