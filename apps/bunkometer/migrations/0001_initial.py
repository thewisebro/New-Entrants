# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0013_auto_20150926_2204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bunk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_code', models.CharField(default=b'xy', max_length=100)),
                ('lec_bunk', models.IntegerField(default=0)),
                ('lec_total', models.IntegerField(default=0)),
                ('tut_bunk', models.IntegerField(default=0)),
                ('tut_total', models.IntegerField(default=0)),
                ('prac_bunk', models.IntegerField(default=0)),
                ('prac_total', models.IntegerField(default=0)),
                ('student', models.ForeignKey(to='nucleus.Student', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_code', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('course_name', models.CharField(max_length=200)),
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
                ('time', models.IntegerField(default=0)),
                ('bunk', models.IntegerField(default=0)),
                ('course_code', models.CharField(default=b'xy', max_length=40)),
                ('course_name', models.CharField(max_length=40)),
                ('class_type', models.IntegerField(default=0)),
                ('student', models.ForeignKey(to='nucleus.Student', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
