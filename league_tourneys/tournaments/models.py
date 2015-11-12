from django.db import models

from lib import challonge, lol

# Create your models here.

class Tournament(models.Model):

    # Database fields
    name = models.CharField(max_length=200)
    challonge_tournament_id = models.IntegerField()
    league_tournament_id = models.IntegerField()

    def __init__(self, name, challonge_settings, lol_settings):
        self.name = name

        # Setup with challonge
        self.challonge_tournament_id = challonge.new_tournament(challonge_settings)
        
        # Setup with league
        self.league_tournament_id = lol.new_tournament(lol_settings)

class Team(models.Model):
    tounament = models.ForeignKey(Tournament)

    # Relationships
    summoners = models.ManyToManyField(Summoner)
     
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

class Summoner(models.Model):
    summoner_id = models.IntegerField()
    summoner_name = models.CharField(max_length=100)
    region_id = models.IntegerField()   #Ignore this for now as we're assuming NA
    
    def __init__(self, name):
        summoner_name = name
        self.suummoner_id = lol.get_summoner_id_for_name(name)


