# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TreatmentMethod.num_of_patients'
        db.add_column(u'medic_treatmentmethod', 'num_of_patients',
                      self.gf('django.db.models.fields.IntegerField')(default=0, blank=True),
                      keep_default=False)

        # Adding field 'TreatmentMethod.histological_type'
        db.add_column(u'medic_treatmentmethod', 'histological_type',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'TreatmentMethod.grade'
        db.add_column(u'medic_treatmentmethod', 'grade',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True),
                      keep_default=False)

        # Adding field 'TreatmentMethod.hormone_receptor_status'
        db.add_column(u'medic_treatmentmethod', 'hormone_receptor_status',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True),
                      keep_default=False)

        # Adding field 'TreatmentMethod.her2_status'
        db.add_column(u'medic_treatmentmethod', 'her2_status',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True),
                      keep_default=False)

        # Adding field 'TreatmentMethod.stage'
        db.add_column(u'medic_treatmentmethod', 'stage',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True),
                      keep_default=False)

        # Adding field 'TreatmentMethod.treatment'
        db.add_column(u'medic_treatmentmethod', 'treatment',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'TreatmentMethod.citation'
        db.add_column(u'medic_treatmentmethod', 'citation',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'TreatmentMethod.organization_name'
        db.add_column(u'medic_treatmentmethod', 'organization_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TreatmentMethod.num_of_patients'
        db.delete_column(u'medic_treatmentmethod', 'num_of_patients')

        # Deleting field 'TreatmentMethod.histological_type'
        db.delete_column(u'medic_treatmentmethod', 'histological_type')

        # Deleting field 'TreatmentMethod.grade'
        db.delete_column(u'medic_treatmentmethod', 'grade')

        # Deleting field 'TreatmentMethod.hormone_receptor_status'
        db.delete_column(u'medic_treatmentmethod', 'hormone_receptor_status')

        # Deleting field 'TreatmentMethod.her2_status'
        db.delete_column(u'medic_treatmentmethod', 'her2_status')

        # Deleting field 'TreatmentMethod.stage'
        db.delete_column(u'medic_treatmentmethod', 'stage')

        # Deleting field 'TreatmentMethod.treatment'
        db.delete_column(u'medic_treatmentmethod', 'treatment')

        # Deleting field 'TreatmentMethod.citation'
        db.delete_column(u'medic_treatmentmethod', 'citation')

        # Deleting field 'TreatmentMethod.organization_name'
        db.delete_column(u'medic_treatmentmethod', 'organization_name')


    models = {
        u'medic.nosology': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Nosology'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        u'medic.treatmentmethod': {
            'Meta': {'ordering': "('nosology',)", 'object_name': 'TreatmentMethod'},
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
            'stage': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'treatment': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['medic']