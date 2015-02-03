# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_celebrityfeed_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('url', models.CharField(max_length=100)),
                ('caption', models.TextField()),
                ('image_url', models.CharField(max_length=255)),
                ('published_on', models.DateTimeField()),
                ('celebrity', models.ForeignKey(related_name='instagram_posts', to='app.Celebrity')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('url', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('image_url', models.CharField(max_length=255)),
                ('celebrity', models.ForeignKey(related_name='tweets', to='app.Celebrity')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
