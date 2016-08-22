# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MirnaMapping.Organism'
        db.add_column(u'mirna_mirnamapping', 'Organism',
                      self.gf('django.db.models.fields.CharField')(default='human', max_length=250),
                      keep_default=False)

        # Adding index on 'MirnaMapping', fields ['miRNA_ID']
        db.create_index(u'mirna_mirnamapping', ['miRNA_ID'])


    def backwards(self, orm):
        # Removing index on 'MirnaMapping', fields ['miRNA_ID']
        db.delete_index(u'mirna_mirnamapping', ['miRNA_ID'])

        # Deleting field 'MirnaMapping.Organism'
        db.delete_column(u'mirna_mirnamapping', 'Organism')


    models = {
        u'mirna.mirnamapping': {
            'Gene': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'Meta': {'object_name': 'MirnaMapping'},
            'Organism': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'Probability': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '2', 'decimal_places': '1'}),
            'Sourse': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miRBase_ID': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'miRNA_ID': ('django.db.models.fields.CharField', [], {'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['mirna']