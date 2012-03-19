# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Druk'
        db.create_table('house_druk', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nr', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('nr_int', self.gf('django.db.models.fields.IntegerField')()),
            ('tytul', self.gf('django.db.models.fields.TextField')()),
            ('opis', self.gf('django.db.models.fields.TextField')()),
            ('dokument_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('house', ['Druk'])

        # Adding M2M table for field druki on 'Punkt'
        db.create_table('house_punkt_druki', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('punkt', models.ForeignKey(orm['house.punkt'], null=False)),
            ('druk', models.ForeignKey(orm['house.druk'], null=False))
        ))
        db.create_unique('house_punkt_druki', ['punkt_id', 'druk_id'])


    def backwards(self, orm):
        
        # Deleting model 'Druk'
        db.delete_table('house_druk')

        # Removing M2M table for field druki on 'Punkt'
        db.delete_table('house_punkt_druki')


    models = {
        'house.druk': {
            'Meta': {'ordering': "['-nr']", 'object_name': 'Druk'},
            'dokument_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nr': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'nr_int': ('django.db.models.fields.IntegerField', [], {}),
            'opis': ('django.db.models.fields.TextField', [], {}),
            'tytul': ('django.db.models.fields.TextField', [], {})
        },
        'house.glosowanie': {
            'Meta': {'ordering': "['time']", 'object_name': 'Glosowanie'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nr': ('django.db.models.fields.IntegerField', [], {}),
            'posiedzenie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['house.Posiedzenie']"}),
            'punkt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['house.Punkt']", 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'tytul': ('django.db.models.fields.TextField', [], {}),
            'wyniki': ('jsonfield.fields.JSONField', [], {'default': '[]'})
        },
        'house.klub': {
            'Meta': {'object_name': 'Klub'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'skrot': ('django.db.models.fields.CharField', [], {'max_length': '16'})
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
            'Meta': {'ordering': "['posiedzenie', 'nr']", 'object_name': 'Punkt'},
            'druki': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['house.Druk']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nr': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'nr_int': ('django.db.models.fields.IntegerField', [], {}),
            'posiedzenie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['house.Posiedzenie']"}),
            'tytul': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['house']
