# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0013_auto_20150926_2204'),
        ('bunkometer', '0004_auto_20151101_1816'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_code', models.CharField(default=b'xy', max_length=100)),
                ('course_name', models.CharField(max_length=200)),
                ('student', models.ForeignKey(to='nucleus.Student', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
