# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import core.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(related_name=b'lectut', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
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
                ('batch', models.ForeignKey(to='nucleus.Batch')),
                ('upload_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
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
                ('event_date', core.models.fields.DateTimeField(default=datetime.datetime(2015, 2, 19, 2, 1, 52, 777984))),
                ('batch', models.ForeignKey(to='nucleus.Batch')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TextNotice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=500)),
                ('batch', models.ForeignKey(to='nucleus.Batch')),
                ('upload_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
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
                ('upload_file', models.FileField(upload_to=b'lectut/images/')),
                ('description', models.CharField(max_length=100)),
                ('file_type', models.CharField(max_length=10)),
                ('upload_type', models.CharField(default=b'tut', max_length=3)),
                ('post', models.ForeignKey(to='lectut.Post')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('upload_file', models.FileField(upload_to=b'lectut/images/')),
                ('name', models.CharField(max_length=100)),
                ('file_type', models.CharField(max_length=10)),
                ('upload_type', models.CharField(default=b'tut', max_length=3)),
                ('privacy', models.BooleanField(default=False)),
                ('batch', models.ForeignKey(to='nucleus.Batch')),
                ('upload_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='downloadlog',
            name='uploadfile',
            field=models.ForeignKey(to='lectut.UploadFile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='downloadlog',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
