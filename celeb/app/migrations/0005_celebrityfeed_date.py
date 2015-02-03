# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_celebrity_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='celebrityfeed',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 1, 20, 7, 18, 30767)),
            preserve_default=False,
        ),
    ]
