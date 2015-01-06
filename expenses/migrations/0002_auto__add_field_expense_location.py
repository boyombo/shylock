# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Expense.location'
        db.add_column('expenses_expense', 'location',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stock.Location'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Expense.location'
        db.delete_column('expenses_expense', 'location_id')


    models = {
        'expenses.category': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'expenses.expense': {
            'Meta': {'ordering': "('date',)", 'object_name': 'Expense'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'expenses'", 'to': "orm['expenses.Category']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stock.Location']", 'null': 'True', 'blank': 'True'})
        },
        'stock.location': {
            'Meta': {'object_name': 'Location'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['expenses']