from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'prequelprizes.views.home', name='home'),
    # url(r'^prequelprizes/', include('prequelprizes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^:3_admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^:3_admin/', include(admin.site.urls)),

    url(r'^$', TemplateView.as_view(template_name="prizes/home.html"), name='home'),
    url(r'^getkey/$', 'prizes.views.get_key'),
    url(r'^checkkey/$', 'prizes.views.check_key'),
    url(r'^details/$', 'prizes.views.enter_details'),
    url(r'^thanks/$', 'prizes.views.thanks'),
    url(r'^guru/samples/$', TemplateView.as_view(template_name="prizes/samples.html")),
)

handler403 = "prizes.views.handler403"