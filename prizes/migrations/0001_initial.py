# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Winner'
        db.create_table('prizes_winner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('creation_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('authentication_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('details_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
        ))
        db.send_create_signal('prizes', ['Winner'])


    def backwards(self, orm):
        # Deleting model 'Winner'
        db.delete_table('prizes_winner')


    models = {
        'prizes.winner': {
            'Meta': {'object_name': 'Winner'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'authentication_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'creation_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'details_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
        }
    }

    complete_apps = ['prizes']