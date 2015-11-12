# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0003_auto_20151112_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='challonge_tournament_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='challonge_tournament_url',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
