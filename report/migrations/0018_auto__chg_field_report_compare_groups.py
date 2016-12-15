# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Report.compare_groups'
        db.alter_column(u'report_report', 'compare_groups', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True))

    def backwards(self, orm):

        # Changing field 'Report.compare_groups'
        db.alter_column(u'report_report', 'compare_groups', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

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
            'compare_groups': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'conclusion_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'corr_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gene_plot': ('django.db.models.fields.CharField', [], {'default': "'vulcano'", 'max_length': '15'}),
            'gene_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'header_data_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_data_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'kinetic_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'logcf_theshold_compare': ('django.db.models.fields.FloatField', [], {'default': '0.2'}),
            'logcf_theshold_plot': ('django.db.models.fields.FloatField', [], {'default': '0.2'}),
            'methods_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'norm_name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'notable_genes': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'organism': ('django.db.models.fields.CharField', [], {'default': "'human'", 'max_length': '5'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'pas_theshold': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'path_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pval_theshold_compare': ('django.db.models.fields.FloatField', [], {'default': '0.05'}),
            'pval_theshold_plot': ('django.db.models.fields.FloatField', [], {'default': '0.05'}),
            'references_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'report_template': ('django.db.models.fields.CharField', [], {'default': "'Original'", 'max_length': '15'}),
            'sim_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'targets_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tf_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'title_short': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        u'report.tfgroup': {
            'Meta': {'object_name': 'TfGroup'},
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['report.Report']"}),
            'trrust': ('django.db.models.fields.files.FileField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['report']