# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0003_auto_20151113_0621'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='started',
            field=models.BooleanField(default=False),
        ),
    ]
