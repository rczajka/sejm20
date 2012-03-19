# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding index on 'Glosowanie', fields ['time']
        db.create_index('house_glosowanie', ['time'])

        # Adding index on 'Druk', fields ['nr_int']
        db.create_index('house_druk', ['nr_int'])

        # Adding index on 'Punkt', fields ['nr_int']
        db.create_index('house_punkt', ['nr_int'])

        # Adding index on 'Klub', fields ['skrot']
        db.create_index('house_klub', ['skrot'])


    def backwards(self, orm):
        
        # Removing index on 'Klub', fields ['skrot']
        db.delete_index('house_klub', ['skrot'])

        # Removing index on 'Punkt', fields ['nr_int']
        db.delete_index('house_punkt', ['nr_int'])

        # Removing index on 'Druk', fields ['nr_int']
        db.delete_index('house_druk', ['nr_int'])

        # Removing index on 'Glosowanie', fields ['time']
        db.delete_index('house_glosowanie', ['time'])


    models = {
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
        'house.klub': {
            'Meta': {'object_name': 'Klub'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'skrot': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'})
        },
        'house.posel': {
            'Meta': {'ordering': "['nazwisko', 'imie']", 'object_name': 'Posel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imie': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'klub': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['house.Klub']", 'null': 'True', 'blank': 'True'}),
            'nazwisko': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
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
        }
    }

    complete_apps = ['house']
