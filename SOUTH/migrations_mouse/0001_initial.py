# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MouseMapping'
        db.create_table(u'mouse_mousemapping', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('human_gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('mouse_gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'mouse', ['MouseMapping'])

        # Adding model 'MousePathway'
        db.create_table(u'mouse_mousepathway', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('amcf', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=2, decimal_places=1)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'mouse', ['MousePathway'])

        # Adding model 'MouseGene'
        db.create_table(u'mouse_mousegene', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('arr', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=2, decimal_places=1)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pathway', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mouse.MousePathway'])),
        ))
        db.send_create_signal(u'mouse', ['MouseGene'])

        # Adding model 'MouseNode'
        db.create_table(u'mouse_mousenode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pathway', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mouse.MousePathway'])),
        ))
        db.send_create_signal(u'mouse', ['MouseNode'])

        # Adding model 'MouseComponent'
        db.create_table(u'mouse_mousecomponent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mouse.MouseNode'])),
        ))
        db.send_create_signal(u'mouse', ['MouseComponent'])

        # Adding model 'MouseRelation'
        db.create_table(u'mouse_mouserelation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reltype', self.gf('django.db.models.fields.CharField')(default=1, max_length=250)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('fromnode', self.gf('django.db.models.fields.related.ForeignKey')(related_name='outrelations', to=orm['mouse.MouseNode'])),
            ('tonode', self.gf('django.db.models.fields.related.ForeignKey')(related_name='inrelations', to=orm['mouse.MouseNode'])),
        ))
        db.send_create_signal(u'mouse', ['MouseRelation'])


    def backwards(self, orm):
        # Deleting model 'MouseMapping'
        db.delete_table(u'mouse_mousemapping')

        # Deleting model 'MousePathway'
        db.delete_table(u'mouse_mousepathway')

        # Deleting model 'MouseGene'
        db.delete_table(u'mouse_mousegene')

        # Deleting model 'MouseNode'
        db.delete_table(u'mouse_mousenode')

        # Deleting model 'MouseComponent'
        db.delete_table(u'mouse_mousecomponent')

        # Deleting model 'MouseRelation'
        db.delete_table(u'mouse_mouserelation')


    models = {
        u'mouse.mousecomponent': {
            'Meta': {'ordering': "['node']", 'object_name': 'MouseComponent'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mouse.MouseNode']"})
        },
        u'mouse.mousegene': {
            'Meta': {'ordering': "['name']", 'object_name': 'MouseGene'},
            'arr': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '2', 'decimal_places': '1'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'pathway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mouse.MousePathway']"})
        },
        u'mouse.mousemapping': {
            'Meta': {'object_name': 'MouseMapping'},
            'human_gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mouse_gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'mouse.mousenode': {
            'Meta': {'ordering': "['pathway']", 'object_name': 'MouseNode'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'pathway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mouse.MousePathway']"})
        },
        u'mouse.mousepathway': {
            'Meta': {'ordering': "['name']", 'object_name': 'MousePathway'},
            'amcf': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '2', 'decimal_places': '1'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        u'mouse.mouserelation': {
            'Meta': {'object_name': 'MouseRelation'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fromnode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'outrelations'", 'to': u"orm['mouse.MouseNode']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reltype': ('django.db.models.fields.CharField', [], {'default': '1', 'max_length': '250'}),
            'tonode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inrelations'", 'to': u"orm['mouse.MouseNode']"})
        }
    }

    complete_apps = ['mouse']