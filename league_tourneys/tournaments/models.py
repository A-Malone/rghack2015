from django.db import models

# Create your models here.

class Tournament(models.Model):
    name = models.CharField(max_length=200)
    link = models.URLField(max_length=200)

class Team(models.Model):
    tounament = models.ForeignKey(Tournament)
    players = models.TextField(max_length=400)
    
    def get_members(self):
        return self.players.split(" ")

class Match(models.Model):
    lol_match_id = models.IntegerField()
