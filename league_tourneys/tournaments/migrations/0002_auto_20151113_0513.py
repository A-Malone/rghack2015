# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='challonge_match_id',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='match',
            name='first_team_id',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='match',
            name='tournament_api_match_id',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='team',
            name='challonge_team_id',
            field=models.IntegerField(default=-1),
        ),
    ]
