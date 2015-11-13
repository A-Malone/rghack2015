# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0007_match_league_match_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='desc',
            field=models.TextField(default=b'', max_length=400),
        ),
        migrations.AddField(
            model_name='tournament',
            name='num_entries',
            field=models.IntegerField(default=0),
        ),
    ]
