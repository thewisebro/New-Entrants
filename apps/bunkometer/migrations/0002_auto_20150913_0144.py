# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bunkometer', '0001_initial'),
    ]

    operations = [
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
        migrations.RenameField(
            model_name='timetable',
            old_name='subject',
            new_name='course_name',
        ),
        migrations.RemoveField(
            model_name='bunk',
            name='subject',
        ),
        migrations.AddField(
            model_name='bunk',
            name='course_code',
            field=models.CharField(default=b'xy', max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bunk',
            name='lec_total',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='timetable',
            name='course_code',
            field=models.CharField(default=b'xy', max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timetable',
            name='class_type',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='time',
            field=models.IntegerField(default=0),
        ),
    ]
