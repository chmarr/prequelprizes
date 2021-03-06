# PrequelPrizes server-side code Copyright (c) 2013 Chris Cogdon - chris@cogdon.org

from django.db import models

class Winner(models.Model):
    key = models.CharField(max_length=32)
    creation_ip = models.IPAddressField()
    creation_time = models.DateTimeField(auto_now_add=True)
    authentication_ip = models.IPAddressField(blank=True, null=True)
    authentication_time = models.DateTimeField(blank=True, null=True)
    details_ip = models.IPAddressField(blank=True, null=True)
    details_time = models.DateTimeField(blank=True, null=True)
    email = models.EmailField(blank=True)
    name = models.CharField(max_length=80, blank=True)
    address1 = models.CharField(max_length=80, blank=True)
    address2 = models.CharField(max_length=80, blank=True)
    city = models.CharField(max_length=80, blank=True)
    state = models.CharField(max_length=80, blank=True)
    postcode = models.CharField(max_length=80, blank=True)
    country = models.CharField(max_length=80, blank=True)
    game_time = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return "%s... (%s, %s)" % ( self.key[:8], self.name, self.email )


class Setting(models.Model):
    key = models.CharField(max_length=80, unique=True)
    value = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        return self.key