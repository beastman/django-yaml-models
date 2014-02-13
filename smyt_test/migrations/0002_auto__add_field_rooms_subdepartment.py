# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Rooms.subdepartment'
        db.add_column(u'smyt_test_rooms', 'subdepartment',
                      self.gf('django.db.models.fields.CharField')(default=' ', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Rooms.subdepartment'
        db.delete_column(u'smyt_test_rooms', 'subdepartment')


    models = {
        'smyt_test.rooms': {
            'Meta': {'object_name': 'Rooms'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spots': ('django.db.models.fields.IntegerField', [], {}),
            'subdepartment': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'smyt_test.users': {
            'Meta': {'object_name': 'Users'},
            'date_joined': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'paycheck': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['smyt_test']