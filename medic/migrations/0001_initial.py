# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Nosology'
        db.create_table(u'medic_nosology', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal(u'medic', ['Nosology'])

        # Adding model 'TreatmentMethod'
        db.create_table(u'medic_treatmentmethod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('nosology', self.gf('django.db.models.fields.related.ForeignKey')(related_name='treatment', to=orm['medic.Nosology'])),
            ('file_pms1', self.gf('django.db.models.fields.files.FileField')(max_length=350)),
            ('file_probability', self.gf('django.db.models.fields.files.FileField')(max_length=350)),
        ))
        db.send_create_signal(u'medic', ['TreatmentMethod'])


    def backwards(self, orm):
        # Deleting model 'Nosology'
        db.delete_table(u'medic_nosology')

        # Deleting model 'TreatmentMethod'
        db.delete_table(u'medic_treatmentmethod')


    models = {
        u'medic.nosology': {
            'Meta': {'object_name': 'Nosology'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        u'medic.treatmentmethod': {
            'Meta': {'object_name': 'TreatmentMethod'},
            'file_pms1': ('django.db.models.fields.files.FileField', [], {'max_length': '350'}),
            'file_probability': ('django.db.models.fields.files.FileField', [], {'max_length': '350'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'nosology': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'treatment'", 'to': u"orm['medic.Nosology']"})
        }
    }

    complete_apps = ['medic']