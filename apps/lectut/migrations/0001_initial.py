# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import core.models.fields
from django.conf import settings
import lectut.models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0003_auto_20150401_0017'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=b'1000')),
                ('privacy', models.BooleanField(default=b'tut', max_length=3)),
                ('deleted', models.BooleanField(default=False)),
                ('batch', models.ForeignKey(to='nucleus.Batch', null=True)),
                ('course', models.ForeignKey(to='nucleus.Course')),
                ('upload_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='post_comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=100)),
                ('post', models.ForeignKey(to='lectut.Post')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reminders',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=50)),
                ('event_date', core.models.fields.DateTimeField(default=datetime.datetime(2015, 4, 8, 0, 22, 0, 400911))),
                ('batch', models.ForeignKey(to='nucleus.Batch')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Uploadedfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('upload_file', models.FileField(upload_to=lectut.models.upload_path)),
                ('description', models.CharField(max_length=100)),
                ('file_type', models.CharField(max_length=10)),
                ('upload_type', models.CharField(default=b'tut', max_length=3)),
                ('deleted', models.BooleanField(default=False)),
                ('download_count', models.IntegerField(default=0)),
                ('post', models.ForeignKey(to='lectut.Post')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='downloadlog',
            name='uploadedfile',
            field=models.ForeignKey(to='lectut.Uploadedfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='downloadlog',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
