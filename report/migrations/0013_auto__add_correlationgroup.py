# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CorrelationGroup'
        db.create_table(u'report_correlationgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('document', self.gf('django.db.models.fields.files.FileField')(max_length=300)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['report.Report'])),
        ))
        db.send_create_signal(u'report', ['CorrelationGroup'])


    def backwards(self, orm):
        # Deleting model 'CorrelationGroup'
        db.delete_table(u'report_correlationgroup')


    models = {
        u'report.correlationgroup': {
            'Meta': {'object_name': 'CorrelationGroup'},
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['report.Report']"})
        },
        u'report.deeplearning': {
            'Meta': {'object_name': 'DeepLearning'},
            'farmclass': ('django.db.models.fields.files.FileField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['report.Report']"}),
            'sideeff': ('django.db.models.fields.files.FileField', [], {'max_length': '300', 'blank': 'True'})
        },
        u'report.genegroup': {
            'Meta': {'object_name': 'GeneGroup'},
            'doc_boxplot': ('django.db.models.fields.files.FileField', [], {'max_length': '300', 'blank': 'True'}),
            'doc_logfc': ('django.db.models.fields.files.FileField', [], {'max_length': '300', 'blank': 'True'}),
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['report.Report']"})
        },
        u'report.pathwaygroup': {
            'Meta': {'object_name': 'PathwayGroup'},
            'doc_proc': ('django.db.models.fields.files.FileField', [], {'max_length': '300', 'blank': 'True'}),
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['report.Report']"})
        },
        u'report.report': {
            'Meta': {'ordering': "['created_at']", 'object_name': 'Report'},
            'compare_groups': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'conclusion_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gene_plot': ('django.db.models.fields.CharField', [], {'default': "'vulcano'", 'max_length': '15'}),
            'gene_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_data_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'methods_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'norm_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'notable_genes': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'organism': ('django.db.models.fields.CharField', [], {'default': "'human'", 'max_length': '5'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'path_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'references_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'title_short': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        u'report.tfgroup': {
            'Meta': {'object_name': 'TfGroup'},
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['report.Report']"})
        }
    }

    complete_apps = ['report']