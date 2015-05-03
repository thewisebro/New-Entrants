# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bunk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=40)),
                ('lec_bunk', models.IntegerField(default=0)),
                ('tut_bunk', models.IntegerField(default=0)),
                ('prac_bunk', models.IntegerField(default=0)),
                ('student', models.ForeignKey(to='nucleus.Student', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.CharField(max_length=9)),
                ('time', models.CharField(max_length=7)),
                ('subject', models.CharField(max_length=40)),
                ('class_type', models.CharField(max_length=4)),
                ('student', models.ForeignKey(to='nucleus.Student', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
