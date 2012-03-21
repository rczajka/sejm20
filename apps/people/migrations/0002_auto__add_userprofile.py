# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserProfile'
        db.create_table('people_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('people', ['UserProfile'])


    def backwards(self, orm):
        
        # Deleting model 'UserProfile'
        db.delete_table('people_userprofile')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 3, 21, 3, 6, 52, 940502)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 3, 21, 3, 6, 52, 940267)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'house.druk': {
            'Meta': {'ordering': "['nr_int']", 'object_name': 'Druk'},
            'dokument_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nr': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'nr_int': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'opis': ('django.db.models.fields.TextField', [], {}),
            'tytul': ('django.db.models.fields.TextField', [], {})
        },
        'house.glosowanie': {
            'Meta': {'ordering': "['time']", 'object_name': 'Glosowanie'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nr': ('django.db.models.fields.IntegerField', [], {}),
            'posiedzenie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['house.Posiedzenie']"}),
            'punkt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['house.Punkt']", 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'tytul': ('django.db.models.fields.TextField', [], {}),
            'wyniki': ('jsonfield.fields.JSONField', [], {'default': '[]'})
        },
        'house.posiedzenie': {
            'Meta': {'ordering': "['-data_start']", 'object_name': 'Posiedzenie'},
            'data_start': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'data_stop': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ilosc_glosowan': ('django.db.models.fields.IntegerField', [], {}),
            'tytul': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'house.punkt': {
            'Meta': {'ordering': "['posiedzenie', 'nr_int']", 'object_name': 'Punkt'},
            'druki': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['house.Druk']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nr': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'nr_int': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'posiedzenie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['house.Posiedzenie']"}),
            'tytul': ('django.db.models.fields.TextField', [], {})
        },
        'people.followship': {
            'Meta': {'unique_together': "[['follower', 'followed']]", 'object_name': 'Followship'},
            'followed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'followers'", 'to': "orm['auth.User']"}),
            'follower': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'follows'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'people.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'people.vote': {
            'Meta': {'ordering': "['-time']", 'unique_together': "[['glosowanie', 'user']]", 'object_name': 'Vote'},
            'glosowanie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['house.Glosowanie']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'vote': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['people']
