# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Document'
        db.create_table(u'profiles_document', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('doc_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('structure', self.gf('jsonfield.fields.JSONField')(default={})),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parameters', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sample_num', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('norm_num', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('row_num', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Project'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='created_by', null=True, to=orm['auth.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('calculated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='calculated_by', null=True, to=orm['auth.User'])),
            ('calculated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'profiles', ['Document'])


        # Changing field 'Project.viewed_at'
        db.alter_column(u'profiles_project', 'viewed_at', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):
        # Deleting model 'Document'
        db.delete_table(u'profiles_document')


        # Changing field 'Project.viewed_at'
        db.alter_column(u'profiles_project', 'viewed_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 4, 17, 0, 0)))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'profiles.document': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'Document'},
            'calculated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'calculated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'calculated_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'created_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'doc_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'norm_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'parameters': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.Project']"}),
            'row_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'sample_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'structure': ('jsonfield.fields.JSONField', [], {'default': '{}'})
        },
        u'profiles.profile': {
            'Meta': {'ordering': "('user',)", 'object_name': 'Profile'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'profiles.project': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'Project'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'members'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'to': u"orm['auth.User']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'viewed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'viewed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'viewed'", 'null': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['profiles']