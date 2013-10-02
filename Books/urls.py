#! -*- coding: UTF-8 -*-
__author__ = 'varnavis'

from django.conf.urls import patterns, include, url
from Books import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'Books.Home.views.load_home', name='load_home'),
    url(r'^feedback/$', 'Books.Home.views.contact', name='contact'),
    url(r'^feedback/thanks/$', 'Books.Home.views.thanks', name='thanks'),
    #url(r'^Books/', include('Books.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^time/$', 'ConstantsDefined.current_datetime2', name='current_datetime2'),
    url(r'^meta/$', 'ConstantsDefined.display_meta', name='display_meta'),
)
