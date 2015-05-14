# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Pathway', fields ['name', 'database']
        db.delete_unique(u'core_pathway', ['name', 'database'])

        # Adding unique constraint on 'Pathway', fields ['name', 'database', 'organism']
        db.create_unique(u'core_pathway', ['name', 'database', 'organism'])


    def backwards(self, orm):
        # Removing unique constraint on 'Pathway', fields ['name', 'database', 'organism']
        db.delete_unique(u'core_pathway', ['name', 'database', 'organism'])

        # Adding unique constraint on 'Pathway', fields ['name', 'database']
        db.create_unique(u'core_pathway', ['name', 'database'])


    models = {
        u'core.component': {
            'Meta': {'ordering': "['node']", 'object_name': 'Component'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Node']"})
        },
        u'core.gene': {
            'Meta': {'ordering': "['name']", 'object_name': 'Gene'},
            'arr': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '2', 'decimal_places': '1'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'pathway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Pathway']"})
        },
        u'core.node': {
            'Meta': {'ordering': "['pathway']", 'object_name': 'Node'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'pathway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Pathway']"})
        },
        u'core.pathway': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'database', 'organism'),)", 'object_name': 'Pathway'},
            'amcf': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '2', 'decimal_places': '1'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'database': ('django.db.models.fields.CharField', [], {'default': "'primary_old'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '350', 'null': 'True', 'blank': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'organism': ('django.db.models.fields.CharField', [], {'default': "'human'", 'max_length': '5'}),
            'pathway_id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        u'core.relation': {
            'Meta': {'object_name': 'Relation'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fromnode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'outrelations'", 'to': u"orm['core.Node']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reltype': ('django.db.models.fields.CharField', [], {'default': '1', 'max_length': '250'}),
            'tonode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inrelations'", 'to': u"orm['core.Node']"})
        }
    }

    complete_apps = ['core']