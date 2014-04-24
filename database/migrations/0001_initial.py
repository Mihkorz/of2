# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pathway'
        db.create_table('pathway', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('amcf', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=2, decimal_places=1)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'database', ['Pathway'])

        # Adding model 'Gene'
        db.create_table('gene', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('arr', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=2, decimal_places=1)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pathway', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['database.Pathway'])),
        ))
        db.send_create_signal(u'database', ['Gene'])

        # Adding model 'Node'
        db.create_table('node', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pathway', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['database.Pathway'])),
        ))
        db.send_create_signal(u'database', ['Node'])

        # Adding model 'Component'
        db.create_table('component', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['database.Node'])),
        ))
        db.send_create_signal(u'database', ['Component'])

        # Adding model 'Relation'
        db.create_table('relation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reltype', self.gf('django.db.models.fields.CharField')(default=1, max_length=250)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('fromnode', self.gf('django.db.models.fields.related.ForeignKey')(related_name='outrelations', to=orm['database.Node'])),
            ('tonode', self.gf('django.db.models.fields.related.ForeignKey')(related_name='inrelations', to=orm['database.Node'])),
        ))
        db.send_create_signal(u'database', ['Relation'])

        # Adding model 'Drug'
        db.create_table('drug', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('tip', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('substance', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('targets', self.gf('django.db.models.fields.CharField')(max_length=350, blank=True)),
            ('morphology', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('price', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sideEffect', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('contraindication', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('compatibility', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('experience', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('isInRussia', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'database', ['Drug'])

        # Adding model 'Target'
        db.create_table('target', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('tip', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('drug', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['database.Drug'])),
        ))
        db.send_create_signal(u'database', ['Target'])


    def backwards(self, orm):
        # Deleting model 'Pathway'
        db.delete_table('pathway')

        # Deleting model 'Gene'
        db.delete_table('gene')

        # Deleting model 'Node'
        db.delete_table('node')

        # Deleting model 'Component'
        db.delete_table('component')

        # Deleting model 'Relation'
        db.delete_table('relation')

        # Deleting model 'Drug'
        db.delete_table('drug')

        # Deleting model 'Target'
        db.delete_table('target')


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