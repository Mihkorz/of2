# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'GOEnrichment'
        db.delete_table(u'database_goenrichment')


    def backwards(self, orm):
        # Adding model 'GOEnrichment'
        db.create_table(u'database_goenrichment', (
            ('Count', self.gf('django.db.models.fields.IntegerField')()),
            ('Term', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('OddsRatio', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('GOID', self.gf('django.db.models.fields.CharField')(max_length=11, null=True, blank=True)),
            ('ontology', self.gf('django.db.models.fields.CharField')(max_length=100)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Pvalue', self.gf('django.db.models.fields.FloatField')()),
            ('ExpCount', self.gf('django.db.models.fields.FloatField')()),
            ('human_pathway', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['database.Pathway'])),
            ('Size', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'database', ['GOEnrichment'])


    models = {
        u'database.component': {
            'Meta': {'ordering': "['node']", 'object_name': 'Component', 'db_table': "'component'"},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['database.Node']"})
        },
        u'database.drug': {
            'Meta': {'ordering': "['name']", 'object_name': 'Drug', 'db_table': "'drug'"},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'compatibility': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contraindication': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'db': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'experience': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'isInRussia': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'morphology': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'price': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sideEffect': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'substance': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'targets': ('django.db.models.fields.CharField', [], {'max_length': '350', 'blank': 'True'}),
            'tip': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        u'database.gene': {
            'Meta': {'ordering': "['name']", 'object_name': 'Gene', 'db_table': "'gene'"},
            'arr': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '2', 'decimal_places': '1'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'pathway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['database.Pathway']"})
        },
        u'database.node': {
            'Meta': {'ordering': "['pathway']", 'object_name': 'Node', 'db_table': "'node'"},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'pathway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['database.Pathway']"})
        },
        u'database.pathway': {
            'Meta': {'ordering': "['name']", 'object_name': 'Pathway', 'db_table': "'pathway'"},
            'amcf': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '2', 'decimal_places': '1'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        u'database.relation': {
            'Meta': {'object_name': 'Relation', 'db_table': "'relation'"},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fromnode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'outrelations'", 'to': u"orm['database.Node']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reltype': ('django.db.models.fields.CharField', [], {'default': '1', 'max_length': '250'}),
            'tonode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inrelations'", 'to': u"orm['database.Node']"})
        },
        u'database.target': {
            'Meta': {'ordering': "['drug']", 'object_name': 'Target', 'db_table': "'target'"},
            'drug': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['database.Drug']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'tip': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['database']