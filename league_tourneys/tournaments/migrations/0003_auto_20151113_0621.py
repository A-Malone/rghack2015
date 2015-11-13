# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0002_auto_20151113_0513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='tournament_api_match_id',
            field=models.CharField(max_length=30),
        ),
    ]
