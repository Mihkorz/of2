# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MetabolismPathway'
        db.create_table(u'metabolism_metabolismpathway', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('pathway_id', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('link_to_picture', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('amcf', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=2, decimal_places=1)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'metabolism', ['MetabolismPathway'])

        # Adding model 'MetabolismGene'
        db.create_table(u'metabolism_metabolismgene', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('arr', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=2, decimal_places=1)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pathway', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metabolism.MetabolismPathway'])),
        ))
        db.send_create_signal(u'metabolism', ['MetabolismGene'])


    def backwards(self, orm):
        # Deleting model 'MetabolismPathway'
        db.delete_table(u'metabolism_metabolismpathway')

        # Deleting model 'MetabolismGene'
        db.delete_table(u'metabolism_metabolismgene')


    models = {
        u'metabolism.metabolismgene': {
            'Meta': {'ordering': "['name']", 'object_name': 'MetabolismGene'},
            'arr': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '2', 'decimal_places': '1'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'pathway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metabolism.MetabolismPathway']"})
        },
        u'metabolism.metabolismpathway': {
            'Meta': {'ordering': "['name']", 'object_name': 'MetabolismPathway'},
            'amcf': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '2', 'decimal_places': '1'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'link_to_picture': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'pathway_id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        }
    }

    complete_apps = ['metabolism']