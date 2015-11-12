# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0002_tournament_challonge_tournament_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('json_text', models.TextField()),
            ],
        ),
        migrations.RenameField(
            model_name='match',
            old_name='tounament',
            new_name='tournament',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='lol_match_id',
            new_name='tournament_api_match_id',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='tounament',
            new_name='tournament',
        ),
    ]
