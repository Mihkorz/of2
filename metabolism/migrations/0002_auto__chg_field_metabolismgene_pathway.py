# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'MetabolismGene.pathway'
        db.alter_column(u'metabolism_metabolismgene', 'pathway_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['metabolism.MetabolismPathway'], null=True))

    def backwards(self, orm):

        # Changing field 'MetabolismGene.pathway'
        db.alter_column(u'metabolism_metabolismgene', 'pathway_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['metabolism.MetabolismPathway']))

    models = {
        u'metabolism.metabolismgene': {
            'Meta': {'ordering': "['name']", 'object_name': 'MetabolismGene'},
            'arr': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '2', 'decimal_places': '1'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'pathway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['metabolism.MetabolismPathway']", 'null': 'True', 'blank': 'True'})
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