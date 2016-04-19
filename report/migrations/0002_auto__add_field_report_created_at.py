# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Report.created_at'
        db.add_column(u'report_report', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2016, 4, 13, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Report.created_at'
        db.delete_column(u'report_report', 'created_at')


    models = {
        u'report.genegroup': {
            'Meta': {'object_name': 'GeneGroup'},
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['report.Report']"})
        },
        u'report.report': {
            'Meta': {'object_name': 'Report'},
            'conclusion_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gene_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_data_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'methods_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'notable_genes': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'path_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'references_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'title_short': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        }
    }

    complete_apps = ['report']