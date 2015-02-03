import dj_database_url
from celeb.base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'instagram',
        'USER': 'instagram',
        'PASSWORD': 'instagram',
        'HOST': 'instagram-1.cykvexeo9jm1.us-east-1.rds.amazonaws.com',
        'PORT': 5432
    }
}

