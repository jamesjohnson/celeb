from celeb.app.models import Publication, Celebrity
import time
import datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "celeb.settings")
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print "Starting"
        total_requests = 0
        total_created = 0
        start_time = time.time()
        for publication in Publication.objects.all():
            publication.update()
        print 'Total time: %.10s' % (time.time() - start_time)
