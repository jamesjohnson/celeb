from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'uniqlo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'celeb.app.views.home', name='home'),
    url(r'^celebrity/(?P<slug>[\w.,/_\-]+)$', 'celeb.app.views.celebrity',
        name='celebrity'),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns('',
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
	    'document_root': settings.STATIC_ROOT,
	}),
)
