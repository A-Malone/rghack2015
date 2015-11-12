from django.db import models

from lib import challonge_api
from lib import tournament_api

# Create your models here.

class Tournament(models.Model):

    # Database fields
    name                        = models.CharField(max_length=200)
    challonge_tournament_id     = models.IntegerField()
    league_tournament_id        = models.IntegerField()
    challonge_tournament_url    = models.CharField(max_length=200)

    def setup(self, challonge_settings):
        # Setup with challonge
        p = challonge_api.create_tournament(challonge_settings)        

        self.challonge_tournament_id = p["tournament"]["id"]
        self.challonge_tournament_url = p["tournament"]["url"]
        
        # Setup with league
        #self.league_tournament_id = tournament_api.new_tournament()
        self.league_tournament_id = -1

class Summoner(models.Model):
    summoner_id = models.IntegerField()
    summoner_name = models.CharField(max_length=100)
    region_id = models.IntegerField()   #Ignore this for now as we're assuming NA
    
    def setup(self):        
        self.summoner_id = tournament_api.get_summoner_id_for_name(self.summoner_name)

class Team(models.Model):
    challonge_team_id           = models.IntegerField()    
    name                        = models.CharField(max_length=100)    

    # Relationships
    tounament = models.ForeignKey(Tournament)
    summoners = models.ManyToManyField(Summoner)

    def __init__(self, name):
        self.name = name

        p = challonge_api.create_participant(tournament.challonge_tournament_id,{"name":name})
        self.challonge_team_id = p['participant']['id']

    def get_members(self):
        players =  self.players.split(" ")
        assert(len(players) == 5)
        return players

class Match(models.Model):    
    tournament_api_match_id = models.IntegerField()

    # Relationships
    teams = models.ManyToManyField(Team)
    tounament = models.ForeignKey(Tournament)

    def __init__(self):
        self.tournament_api_match_id = -1

    def create_match(self):
        """ Lazy loading of matches on call """
        self.tournament_api_match_id = tournament_api.get_tournament_code()


class Notification(models.Model):
    json_text = models.TextField()