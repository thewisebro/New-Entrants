# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bunk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rollNum', models.CharField(default=b'13115100', max_length=15)),
                ('subject', models.CharField(max_length=40)),
                ('lec_bunk', models.IntegerField(default=0)),
                ('tut_bunk', models.IntegerField(default=0)),
                ('prac_bunk', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rollNum', models.CharField(default=b'13115100', max_length=15)),
                ('day', models.CharField(max_length=9)),
                ('time', models.TimeField()),
                ('subject', models.CharField(max_length=40)),
                ('class_type', models.CharField(max_length=3)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
