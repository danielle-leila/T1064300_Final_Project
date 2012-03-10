from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from albums.views import *


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'coffeeTable.views.home', name='home'),
    # url(r'^coffeeTable/', include('coffeeTable.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # Home page >> welcome, create_album or albums
    url(u'^$', index),
    
    url(r'^create_album/$', initiate_album),
    
    url(r'^create_album/(?P<page_no>\d+)/$', get_template),
    
    url(r'^create_album/(?P<page_no>\d+)/(?P<template>.+)/$', create_page),
    
 
    
)
