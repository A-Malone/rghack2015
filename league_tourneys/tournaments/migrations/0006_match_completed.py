# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0005_auto_20151113_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
