# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Vote.comment'
        db.add_column(u'polls_vote', 'comment',
                      self.gf('django.db.models.fields.TextField')(max_length=144, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Vote.datetime'
        db.add_column(u'polls_vote', 'datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2015, 2, 19, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Vote.data'
        db.add_column(u'polls_vote', 'data',
                      self.gf('django.db.models.fields.TextField')(default='{}', null=True, blank=True),
                      keep_default=False)

        # Adding field 'Poll.is_closed'
        db.add_column(u'polls_poll', 'is_closed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Poll.reference'
        db.add_column(u'polls_poll', 'reference',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=36, blank=True, unique=True),
                      keep_default=False)
        # mysql error:
        # Duplicate index 'polls_poll_reference_4cacbf22888a7509_uniq' defined on the table 'polls.polls_poll
        #db.create_unique(u'polls_poll', ['reference'])

        # Adding field 'Poll.is_multiple'
        db.add_column(u'polls_poll', 'is_multiple',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Poll.is_anonymous'
        db.add_column(u'polls_poll', 'is_anonymous',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Poll.start_votes'
        db.add_column(u'polls_poll', 'start_votes',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 2, 19, 0, 0)),
                      keep_default=False)

        # Adding field 'Poll.end_votes'
        db.add_column(u'polls_poll', 'end_votes',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 2, 24, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Vote.comment'
        db.delete_column(u'polls_vote', 'comment')

        # Deleting field 'Vote.datetime'
        db.delete_column(u'polls_vote', 'datetime')

        # Deleting field 'Vote.data'
        db.delete_column(u'polls_vote', 'data')

        # Deleting field 'Poll.is_closed'
        db.delete_column(u'polls_poll', 'is_closed')

        # Deleting field 'Poll.reference'
        db.delete_column(u'polls_poll', 'reference')
        #db.delete_unique(u'polls_poll', ['reference'])

        # Deleting field 'Poll.is_multiple'
        db.delete_column(u'polls_poll', 'is_multiple')

        # Deleting field 'Poll.is_anonymous'
        db.delete_column(u'polls_poll', 'is_anonymous')

        # Deleting field 'Poll.start_votes'
        db.delete_column(u'polls_poll', 'start_votes')

        # Deleting field 'Poll.end_votes'
        db.delete_column(u'polls_poll', 'end_votes')


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
        u'polls.choice': {
            'Meta': {'ordering': "['choice']", 'object_name': 'Choice'},
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Poll']"})
        },
        u'polls.poll': {
            'Meta': {'ordering': "['-start_votes']", 'object_name': 'Poll'},
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_votes': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 2, 24, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_multiple': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True', 'unique': 'True'}),
            'start_votes': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 2, 19, 0, 0)'})
        },
        u'polls.vote': {
            'Meta': {'unique_together': "(('user', 'poll'),)", 'object_name': 'Vote'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Choice']"}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '144', 'null': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.Poll']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['polls']