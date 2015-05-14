# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pathway'
        db.create_table(u'core_pathway', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pathway_id', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('organism', self.gf('django.db.models.fields.CharField')(default='human', max_length=5)),
            ('database', self.gf('django.db.models.fields.CharField')(default='primary_old', max_length=20)),
            ('amcf', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=2, decimal_places=1)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=350, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Pathway'])

        # Adding model 'Gene'
        db.create_table(u'core_gene', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('arr', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=2, decimal_places=1)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pathway', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Pathway'])),
        ))
        db.send_create_signal(u'core', ['Gene'])

        # Adding model 'Node'
        db.create_table(u'core_node', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pathway', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Pathway'])),
        ))
        db.send_create_signal(u'core', ['Node'])

        # Adding model 'Component'
        db.create_table(u'core_component', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Node'])),
        ))
        db.send_create_signal(u'core', ['Component'])

        # Adding model 'Relation'
        db.create_table(u'core_relation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reltype', self.gf('django.db.models.fields.CharField')(default=1, max_length=250)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('fromnode', self.gf('django.db.models.fields.related.ForeignKey')(related_name='outrelations', to=orm['core.Node'])),
            ('tonode', self.gf('django.db.models.fields.related.ForeignKey')(related_name='inrelations', to=orm['core.Node'])),
        ))
        db.send_create_signal(u'core', ['Relation'])


    def backwards(self, orm):
        # Deleting model 'Pathway'
        db.delete_table(u'core_pathway')

        # Deleting model 'Gene'
        db.delete_table(u'core_gene')

        # Deleting model 'Node'
        db.delete_table(u'core_node')

        # Deleting model 'Component'
        db.delete_table(u'core_component')

        # Deleting model 'Relation'
        db.delete_table(u'core_relation')


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
            'Meta': {'ordering': "['name']", 'object_name': 'Pathway'},
            'amcf': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '2', 'decimal_places': '1'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'database': ('django.db.models.fields.CharField', [], {'default': "'primary_old'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '350', 'null': 'True', 'blank': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
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