# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0003_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='tournament_code',
            field=models.TextField(default=b''),
        ),
    ]
