# PrequelPrizes server-side code Copyright (c) 2013 Chris Cogdon - chris@cogdon.org

import re
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'prequelprizes.views.home', name='home'),
    # url(r'^prequelprizes/', include('prequelprizes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^' + re.escape(settings.ADMIN_URL[1:]) + 'doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^' + re.escape(settings.ADMIN_URL[1:]), include(admin.site.urls)),

    url(r'^$', TemplateView.as_view(template_name="prizes/home.html"), name='home'),
    url(r'^getkey/$', 'prizes.views.get_key'),
    url(r'^checkkey/$', 'prizes.views.check_key'),
    url(r'^details/$', 'prizes.views.enter_details'),
    url(r'^thanks/$', 'prizes.views.thanks'),

    url(r'^csvdump/$', 'prizes.views.csv_dump'),
)

handler403 = "prizes.views.handler403"