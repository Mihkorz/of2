# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Report'
        db.create_table(u'report_report', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('title_short', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('input_data_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('methods_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('gene_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('path_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('conclusion_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('references_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('notable_genes', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal(u'report', ['Report'])

        # Adding model 'GeneGroup'
        db.create_table(u'report_genegroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('document', self.gf('django.db.models.fields.files.FileField')(max_length=300)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['report.Report'])),
        ))
        db.send_create_signal(u'report', ['GeneGroup'])


    def backwards(self, orm):
        # Deleting model 'Report'
        db.delete_table(u'report_report')

        # Deleting model 'GeneGroup'
        db.delete_table(u'report_genegroup')


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