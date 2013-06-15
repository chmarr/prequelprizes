from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'prequelprizes.views.home', name='home'),
    # url(r'^prequelprizes/', include('prequelprizes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^getkey/', 'prizes.views.get_key'),
    url(r'^checkkey/', 'prizes.views.check_key'),
    url(r'^details/', 'prizes.views.enter_details'),
    url(r'^thanks/', 'prizes.views.thanks'),
    url(r'^guru/', 'prizes.views.guru_error'),
)

handler403 = "prizes.views.handler403"