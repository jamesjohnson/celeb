import dj_database_url
from celeb.base import *

DEBUG = False

DATABASES['default'] =  dj_database_url.config()
