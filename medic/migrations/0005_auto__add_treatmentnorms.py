# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TreatmentNorms'
        db.create_table(u'medic_treatmentnorms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('nosology', self.gf('django.db.models.fields.related.ForeignKey')(related_name='norms', to=orm['medic.Nosology'])),
            ('num_of_norms', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('file_norms', self.gf('django.db.models.fields.files.FileField')(max_length=350)),
        ))
        db.send_create_signal(u'medic', ['TreatmentNorms'])


    def backwards(self, orm):
        # Deleting model 'TreatmentNorms'
        db.delete_table(u'medic_treatmentnorms')


    models = {
        u'medic.nosology': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Nosology'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        u'medic.treatmentmethod': {
            'Meta': {'ordering': "('nosology',)", 'object_name': 'TreatmentMethod'},
            'accuracy': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'citation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file_pms1': ('django.db.models.fields.files.FileField', [], {'max_length': '350'}),
            'file_probability': ('django.db.models.fields.files.FileField', [], {'max_length': '350'}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'her2_status': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'histological_type': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'hormone_receptor_status': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'nosology': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'treatment'", 'to': u"orm['medic.Nosology']"}),
            'num_of_patients': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'organization_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'percentage_response': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ref_clinical_trial': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'stage': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'treatment': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'medic.treatmentnorms': {
            'Meta': {'object_name': 'TreatmentNorms'},
            'file_norms': ('django.db.models.fields.files.FileField', [], {'max_length': '350'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'nosology': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'norms'", 'to': u"orm['medic.Nosology']"}),
            'num_of_norms': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['medic']