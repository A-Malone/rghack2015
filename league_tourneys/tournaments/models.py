from django.db import models

from lib import challonge_api
from lib import tournament_api
from lib import utils

# Create your models here.

class Tournament(models.Model):

    # Database fields
    name                        = models.CharField(max_length=200)
    league_tournament_id        = models.IntegerField()
    challonge_tournament_id     = models.IntegerField(null=True)
    challonge_tournament_url    = models.CharField(max_length=200, null=True)
    started                     = models.BooleanField(default=False)

    def setup(self, challonge_settings):
        # Setup with challonge
        challonge_settings.pop("tournament_type")
        p = challonge_api.create_tournament(challonge_settings)        

        self.challonge_tournament_id = p["tournament"]["id"]
        self.challonge_tournament_url = p["tournament"]["url"]
        
        # Setup with league
        self.league_tournament_id = tournament_api.create_tournament(self.name)


    def start(self):
        challonge_api.start_tournament(self.challonge_tournament_id)        
        self.started=True
        tournament.update_available_matches()
        self.save()

    def update_available_matches(self):
        p = challonge_api.get_match_list(self.challonge_tournament_id, state="open")

        for match_json in p:
            challonge_match_id = match_json["match"]["id"]
            player1_id = match_json["match"]["player1_id"]
            player2_id = match_json["match"]["player2_id"]

            if(not self.match_set.filter(challonge_match_id=challonge_match_id)):
                match = Match.create(self, challonge_match_id, player1_id, player2_id)
                self.match_set.add(match)

    def __repr__(self):
        return "Tournament: {}".format(self.name)

class Summoner(models.Model):
    summoner_id = models.IntegerField()
    summoner_name = models.CharField(max_length=100)
    region_id = models.IntegerField()   #Ignore this for now as we're assuming NA

    @classmethod
    def find_or_create(cls, name):        
        summoners = Summoner.objects.filter(summoner_name=name)
        if(summoners):
            return summoners.first()

        summoner_id = tournament_api.summoner_name_to_id(name)
        summoner = Summoner(summoner_name=name, summoner_id=summoner_id, region_id=0)
        summoner.save()
        return summoner
    
    def __repr__(self):
        return "Summoner: {}".format(self.summoner_name)

class Team(models.Model):
    challonge_team_id           = models.IntegerField(default=-1)
    name                        = models.CharField(max_length=100)
    # Relationships
    tournament                  = models.ForeignKey(Tournament)
    summoners                   = models.ManyToManyField(Summoner)

    @classmethod
    def create(cls, name, tournament):        
        team = Team(name=name)
        
        tournament.team_set.add(team)

        p = challonge_api.create_participant(tournament.challonge_tournament_id, {'name':name, 'misc':int(team.pk)})
        team.challonge_team_id = p["participant"]["id"]
        team.save()

        return team
        
    def __repr__(self):
        return "Team: {}".format(self.name)
    
class Match(models.Model):
    tournament_api_match_id     = models.CharField(max_length=30)
    challonge_match_id          = models.IntegerField(default=-1)
    first_team_id               = models.IntegerField(default=-1)   #First team in challonge
    # Relationships
    teams                       = models.ManyToManyField(Team)
    tournament                  = models.ForeignKey(Tournament)

    @classmethod
    def create(cls, tournament, challonge_match_id, team_1, team_2):
        match = Match(challonge_match_id=challonge_match_id, tournament_id=tournament.pk)                
        
        # Add teams
        first_team = Team.objects.get(challonge_team_id=team_1)
        first_team_id = first_team.pk
        match.save()

        match.teams.add(first_team)
        match.teams.add(Team.objects.get(challonge_team_id=team_2))
        match.save()

        summ_ids = []
        for team in match.teams.all():            
            for player in team.summoners.all():
                summ_ids.append(player.summoner_id)    

        # Create the match
        match.tournament_api_match_id = tournament_api.create_match(tournament.league_tournament_id, allowed_ids=summ_ids)
        match.save()

        return match
    
    def __repr__(self):
        return "Match: {}".format(self.tournament_api_match_id)

class Notification(models.Model):
    tournament_code = models.TextField(default='')
    json_text = models.TextField()

