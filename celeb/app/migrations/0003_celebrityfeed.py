# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('app', '0002_auto_20150130_1604'),
    ]

    operations = [
        migrations.CreateModel(
            name='CelebrityFeed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('target_id', models.PositiveIntegerField(null=True, blank=True)),
                ('score', models.DecimalField(default=0, max_digits=10, decimal_places=4)),
                ('celebrity', models.ForeignKey(related_name='feed', to='app.Celebrity')),
                ('target_ct', models.ForeignKey(related_name='feed_target', blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
