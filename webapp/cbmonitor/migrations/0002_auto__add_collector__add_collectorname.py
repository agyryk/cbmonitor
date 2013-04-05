# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Collector'
        db.create_table('cbmonitor_collector', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cbmonitor.CollectorName'])),
            ('interval', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cbmonitor.Cluster'])),
        ))
        db.send_create_signal('cbmonitor', ['Collector'])

        # Adding model 'CollectorName'
        db.create_table('cbmonitor_collectorname', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, primary_key=True)),
        ))
        db.send_create_signal('cbmonitor', ['CollectorName'])

    def backwards(self, orm):
        # Deleting model 'Collector'
        db.delete_table('cbmonitor_collector')

        # Deleting model 'CollectorName'
        db.delete_table('cbmonitor_collectorname')

    models = {
        'cbmonitor.bucket': {
            'Meta': {'unique_together': "(['name', 'cluster'],)", 'object_name': 'Bucket'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cbmonitor.Cluster']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '32'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'port': ('django.db.models.fields.IntegerField', [], {'default': '11211', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cbmonitor.BucketType']"})
        },
        'cbmonitor.buckettype': {
            'Meta': {'object_name': 'BucketType'},
            'type': ('django.db.models.fields.CharField', [], {'max_length': '9', 'primary_key': 'True'})
        },
        'cbmonitor.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'master_node': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'}),
            'rest_password': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'rest_username': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'cbmonitor.collector': {
            'Meta': {'object_name': 'Collector'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cbmonitor.Cluster']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cbmonitor.CollectorName']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'cbmonitor.collectorname': {
            'Meta': {'object_name': 'CollectorName'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'primary_key': 'True'})
        },
        'cbmonitor.observable': {
            'Meta': {'unique_together': "(['name', 'cluster', 'server', 'bucket'],)", 'object_name': 'Observable'},
            'bucket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cbmonitor.Bucket']", 'null': 'True', 'blank': 'True'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cbmonitor.Cluster']"}),
            'collector': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cbmonitor.Server']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cbmonitor.ObservableType']"}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'cbmonitor.observabletype': {
            'Meta': {'object_name': 'ObservableType'},
            'type': ('django.db.models.fields.CharField', [], {'max_length': '6', 'primary_key': 'True'})
        },
        'cbmonitor.server': {
            'Meta': {'object_name': 'Server'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '80', 'primary_key': 'True'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cbmonitor.Cluster']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'ssh_key': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'blank': 'True'}),
            'ssh_password': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'ssh_username': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        'cbmonitor.snapshot': {
            'Meta': {'object_name': 'Snapshot'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cbmonitor.Cluster']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'}),
            'ts_from': ('django.db.models.fields.DateTimeField', [], {}),
            'ts_to': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['cbmonitor']
