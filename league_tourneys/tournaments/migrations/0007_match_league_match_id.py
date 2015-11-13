# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0006_match_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='league_match_id',
            field=models.IntegerField(default=-1),
        ),
    ]
