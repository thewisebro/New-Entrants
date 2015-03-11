# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacSpace',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('space', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Honors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('year', models.CharField(max_length=10, null=True, blank=True)),
                ('award', models.CharField(max_length=100)),
                ('institute', models.CharField(max_length=100)),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
                ('faculty', models.ForeignKey(to='nucleus.Faculty')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
