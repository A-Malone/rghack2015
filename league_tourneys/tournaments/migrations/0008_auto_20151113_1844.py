# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0007_match_league_match_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='tournament_api_match_id',
            field=models.CharField(max_length=50),
        ),
    ]
