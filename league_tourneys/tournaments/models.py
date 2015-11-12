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

    def setup(self, challonge_settings, lol_settings):
        # Setup with challonge
        p = challonge_api.create_tournament(challonge_settings)
        self.challonge_tournament_id = p["tournament"]["id"]
        self.challonge_tournament_url = p["tournament"]["url"]
        
        # Setup with league
        self.league_tournament_id = lol.new_tournament(lol_settings)


class Summoner(models.Model):
    summoner_id = models.IntegerField()
    summoner_name = models.CharField(max_length=100)
    region_id = models.IntegerField()   #Ignore this for now as we're assuming NA
    
    def __init__(self, name):
        summoner_name = name
        self.suummoner_id = lol.get_summoner_id_for_name(name)

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
    teams = models.TextField(max_length=200)
    lol_match_id = models.IntegerField()

    # Relationships
    teams = models.ManyToManyField(Team)
    tounament = models.ForeignKey(Tournament)

    def __init__(self):
        self.lol_match_id = -1

    def create_match(self):
        """ Lazy loading of matches on call """
        self.lol_match_id = lol.get_tournament_code()



