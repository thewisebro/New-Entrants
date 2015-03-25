# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('gamecode', models.CharField(max_length=100)),
                ('score', models.IntegerField()),
                ('student', models.ForeignKey(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('gamecode', models.CharField(max_length=100)),
                ('gsession', models.CharField(max_length=100)),
                ('start_time', core.models.fields.DateTimeField(auto_now_add=True)),
                ('authkey', models.CharField(max_length=100)),
                ('student', models.ForeignKey(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
