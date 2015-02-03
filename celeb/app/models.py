import requests
from itertools import chain
import instagram
import random
import feedparser
import math
import os
import time
from datetime import datetime,timedelta
import re
import string
import random
import lxml.html
from dateutil import parser

from difflib import get_close_matches
from django.core.mail import EmailMultiAlternatives
from django.core.files import File
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.contrib.auth.models import AbstractUser, UserManager
from django.template.defaultfilters import slugify

from django.conf import settings


def slugify(s):
    alphanumeric = re.compile(r'[^a-zA-Z0-9]+')
    slug = alphanumeric.sub('-', s.lower()).strip('-')[:35]
    if len(slug) == 0:
        return random.choice(string.lowercase)
    return slug

class TimeStampedModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Celebrity(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    twitter_username = models.CharField(max_length=100, null=True, blank=True)
    instagram_username = models.CharField(max_length=100, null=True, blank=True)
    scraper_name = models.CharField(max_length=100, null=True, blank=True)
    articles = models.ManyToManyField("Article", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            self.slug = slug
        super(Celebrity, self).save(*args, **kwargs)

    @property
    def first_image(self):
        try:
            first_story = self.feed.exclude(image_url=None)[0]
            return first_story.image_url
        except:
            return None

    @property
    def get_absolute_url(self):
        return "/celebrity/{}".format(self.slug)

    def get_twitter_posts(self):
        pass

    def get_instagram_posts(self):
        INSTAGRAM_ACCESS_TOKEN ="4876791.98b8b06.22738181fcf54fc08e8043f646524635"
        api = instagram.client.InstagramAPI(access_token=INSTAGRAM_ACCESS_TOKEN)
        user = api.user_search(q=self.instagram_username)[0]
        medias, _ = api.user_recent_media(user_id=user.id)
        for media in medias:
            photo, _ = InstagramPost.objects.get_or_create(image_url=media.images['standard_resolution'].url,
                    celebrity=self,
                    defaults={
                        "url":media.link,
                        "caption":'',
                        "published_on":media.created_time})
            if hasattr(media.caption, 'text'):
                photo.caption=media.caption.text
            photo.save()

    @property
    def organized_feed(self):
        feed = self.feed.all()
        instagram_posts = feed.filter(target_ct__name='instagram post')[:4]
        articles = feed.filter(target_ct__name='article')
        return sorted(
                chain(instagram_posts, articles),
                key=lambda instance: instance.date, reverse=True)

    @property
    def names(self):
        return [s.lower() for s in self.scraper_name.split(",")]

    @property
    def clean_name(self):
        return self.name.lower()

    def __unicode__(self):
        return self.name

class CelebrityFeed(TimeStampedModel):
    celebrity = models.ForeignKey(Celebrity, related_name='feed')

    target_ct = models.ForeignKey(ContentType, related_name='feed_target', null=True, blank=True)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = generic.GenericForeignKey('target_ct', 'target_id')

    score = models.DecimalField(default=0, decimal_places=4, max_digits=10)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.celebrity.name


class Article(TimeStampedModel):
    publication = models.ForeignKey("Publication")
    title = models.CharField(max_length=255, unique=True)
    link = models.TextField()
    image_url = models.URLField(null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    published_on = models.DateTimeField()
    slug = models.CharField(max_length=128, null=True, blank=True)
    summary = models.TextField()

    def tag_celebrities(self, celebrities):
        found_celebrities = []
        text = self.summary.lower() + self.title.lower()
        for celebrity in celebrities:
            if any(name in text for name in celebrity[1]):
                found_celebrities.append(celebrity[0])
        celebrities = Celebrity.objects.filter(id__in=found_celebrities)
        for celebrity in celebrities:
            celebrity.articles.add(self)
            type = ContentType.objects.get_for_model(self)
            CelebrityFeed.objects.get_or_create(celebrity=celebrity,
                    target_ct=type, target_id=self.id)
        return len(found_celebrities)


    def __unicode__(self):
        return self.title

class Tweet(TimeStampedModel):
    celebrity = models.ForeignKey(Celebrity, related_name='tweets')
    url = models.CharField(max_length=100)
    text = models.TextField()
    image_url = models.CharField(max_length=255)

    def __unicode__(self):
        return self.image_url


class InstagramPost(TimeStampedModel):
    celebrity = models.ForeignKey(Celebrity, related_name='instagram_posts')
    url = models.CharField(max_length=100)
    caption = models.TextField()
    image_url = models.CharField(max_length=255)
    published_on = models.DateTimeField()

    def __unicode__(self):
        return self.image_url

class Publication(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)
    short_name = models.CharField(max_length=32, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    rss_feed = models.CharField(max_length=255)

    class Meta():
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def update(self):
        celebrities = [(c.id, c.names) for c in Celebrity.objects.all()]
        count = 0
        print "feed started"
        data = feedparser.parse(self.rss_feed)
        for item in data['items']:
            title = item.get('title')
            link = item.get('link')
            page = requests.get(link)
            root = lxml.html.fromstring(page.content)
            try:
                img = root.xpath('/html/head/meta[@property="og:image"][1]/@content')[0]
            except Exception, e:
                print e
            summary = item.get('summary')
            if not summary:
                summary = item.get('description')

            if summary:
                doc = lxml.html.fromstring(summary)
                summary = doc.text_content()
            updated_on = None
            try:
                updated_on = parser.parse(item.get('updated_parsed'))
            except:
                try:
                    updated_on = parser.parse(item.get('pubDate'))
                except:
                    pass
            if not updated_on:
                updated_on = datetime.now()
            article, _ = Article.objects.get_or_create(
                    title=title,
                    publication=self,
                    defaults={
                        'publication': self,
                        'image_url': img,
                        'published_on': updated_on,
                        'link': link,
                        'summary': summary,
                    })
            found = article.tag_celebrities(celebrities)
            print "We found %s celebrities in %s" % (found, article.title)

