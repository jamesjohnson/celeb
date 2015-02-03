import dj_database_url
from celeb.base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'celeb',
        'USER': 'celeb',
        'PASSWORD': 'celeb123',
    }
}

