# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lol_match_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Summoner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('summoner_id', models.IntegerField()),
                ('summoner_name', models.CharField(max_length=100)),
                ('region_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('challonge_team_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('summoners', models.ManyToManyField(to='tournaments.Summoner')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('challonge_tournament_id', models.IntegerField()),
                ('league_tournament_id', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='tounament',
            field=models.ForeignKey(to='tournaments.Tournament'),
        ),
        migrations.AddField(
            model_name='match',
            name='teams',
            field=models.ManyToManyField(to='tournaments.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='tounament',
            field=models.ForeignKey(to='tournaments.Tournament'),
        ),
    ]
