# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(unique=True, max_length=255)),
                ('link', models.TextField()),
                ('image_url', models.URLField(null=True, blank=True)),
                ('content', models.TextField(null=True, blank=True)),
                ('published_on', models.DateTimeField()),
                ('slug', models.CharField(max_length=128, null=True, blank=True)),
                ('summary', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Celebrity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('twitter_username', models.CharField(max_length=100, null=True, blank=True)),
                ('instagram_username', models.CharField(max_length=100, null=True, blank=True)),
                ('scraper_name', models.CharField(max_length=100, null=True, blank=True)),
                ('articles', models.ManyToManyField(to='app.Article', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('short_name', models.CharField(max_length=32, null=True, blank=True)),
                ('link', models.CharField(max_length=255, null=True, blank=True)),
                ('rss_feed', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='article',
            name='publication',
            field=models.ForeignKey(to='app.Publication'),
            preserve_default=True,
        ),
    ]
