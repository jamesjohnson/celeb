import logging
import smtplib
import math
import json
import re
import os
import tweepy
from functools import wraps

from django.shortcuts import get_object_or_404
from django.shortcuts import render as django_render
from django.shortcuts import redirect
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.template import Context, Template
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import *
from django.conf import settings

def render_to_or_json(template):
    def k(fun):
        @wraps(fun)
        def wrapper(request, *args, **kwargs):
            context = fun(request, *args, **kwargs)
            if type(context) == dict:
                if request.is_ajax():
                    return JsonResponse(context)
                else:
                    return django_render(request, template, context)
            else:
                return context
        return wrapper
    return k

@render_to_or_json("home.html")
def home(request):
    celebrities = Celebrity.objects.all()
    return {"celebrities": celebrities}

@render_to_or_json("celebrity.html")
def celebrity(request, slug):
    celebrity = Celebrity.objects.get(slug=slug)
    other_celebs = Celebrity.objects.all()[:10]
    articles = celebrity.organized_feed
    return {"articles": articles,
            "other_celebs": other_celebs,
            "celebrity": celebrity}


