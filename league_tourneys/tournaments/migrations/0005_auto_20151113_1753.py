# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0004_tournament_started'),
    ]

    operations = [
        migrations.AddField(
            model_name='summoner',
            name='league',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AddField(
            model_name='summoner',
            name='summoner_icon',
            field=models.IntegerField(default=1),
        ),
    ]
