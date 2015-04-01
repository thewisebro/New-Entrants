# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('person', models.ForeignKey(related_name=b'feedback_person', to='nucleus.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bhawan', models.CharField(max_length=10, choices=[(b'AZB', b'Azad Bhawan'), (b'CTB', b'Cautley Bhawan'), (b'GNB', b'Ganga Bhawan'), (b'GVB', b'Govind Bhawan'), (b'JWB', b'Jawahar Bhawan'), (b'RKB', b'Radhakrishnan Bhawan'), (b'RJB', b'Rajendra Bhawan'), (b'RGB', b'Rajiv Bhawan'), (b'RVB', b'Ravindra Bhawan'), (b'MVB', b'Malviya Bhawan'), (b'SB', b'Sarojini Bhawan'), (b'KB', b'Kasturba Bhawan'), (b'IB', b' Indra Bhawan')])),
                ('date', models.DateField(default=datetime.date(2015, 3, 25))),
                ('time_of_day', models.IntegerField(default=0)),
                ('content', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('sum_ratings', models.IntegerField(default=0)),
                ('count_ratings', models.IntegerField(default=0)),
                ('raters', models.CharField(max_length=1000, null=True, blank=True)),
            ],
            options={
                'ordering': ('time_of_day', 'date'),
            },
            bases=(models.Model,),
        ),
    ]
