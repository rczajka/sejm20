# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Klub'
        db.create_table('house_klub', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nazwa', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('skrot', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('house', ['Klub'])

        # Adding model 'Posel'
        db.create_table('house_posel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('imie', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('nazwisko', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('klub', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['house.Klub'], null=True, blank=True)),
        ))
        db.send_create_signal('house', ['Posel'])

        # Adding model 'Posiedzenie'
        db.create_table('house_posiedzenie', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tytul', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('data_start', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('data_stop', self.gf('django.db.models.fields.DateField')()),
            ('ilosc_glosowan', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('house', ['Posiedzenie'])

        # Adding model 'Punkt'
        db.create_table('house_punkt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('posiedzenie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['house.Posiedzenie'])),
            ('nr', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('nr_int', self.gf('django.db.models.fields.IntegerField')()),
            ('tytul', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('house', ['Punkt'])

        # Adding model 'Glosowanie'
        db.create_table('house_glosowanie', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('posiedzenie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['house.Posiedzenie'])),
            ('punkt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['house.Punkt'], null=True, blank=True)),
            ('nr', self.gf('django.db.models.fields.IntegerField')()),
            ('tytul', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('wyniki', self.gf('jsonfield.fields.JSONField')(default=[])),
        ))
        db.send_create_signal('house', ['Glosowanie'])


    def backwards(self, orm):
        
        # Deleting model 'Klub'
        db.delete_table('house_klub')

        # Deleting model 'Posel'
        db.delete_table('house_posel')

        # Deleting model 'Posiedzenie'
        db.delete_table('house_posiedzenie')

        # Deleting model 'Punkt'
        db.delete_table('house_punkt')

        # Deleting model 'Glosowanie'
        db.delete_table('house_glosowanie')


    models = {
        'house.glosowanie': {
            'Meta': {'ordering': "['time']", 'object_name': 'Glosowanie'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nr': ('django.db.models.fields.IntegerField', [], {}),
            'posiedzenie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['house.Posiedzenie']"}),
            'punkt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['house.Punkt']", 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'tytul': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nr': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'nr_int': ('django.db.models.fields.IntegerField', [], {}),
            'posiedzenie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['house.Posiedzenie']"}),
            'tytul': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['house']
