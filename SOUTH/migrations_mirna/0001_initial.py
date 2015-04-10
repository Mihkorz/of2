# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MirnaMapping'
        db.create_table(u'mirna_mirnamapping', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('miRNA_ID', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('miRBase_ID', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('Gene', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('Probability', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=2, decimal_places=1)),
            ('Sourse', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'mirna', ['MirnaMapping'])


    def backwards(self, orm):
        # Deleting model 'MirnaMapping'
        db.delete_table(u'mirna_mirnamapping')


    models = {
        u'mirna.mirnamapping': {
            'Gene': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'Meta': {'object_name': 'MirnaMapping'},
            'Probability': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '2', 'decimal_places': '1'}),
            'Sourse': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miRBase_ID': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'miRNA_ID': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['mirna']