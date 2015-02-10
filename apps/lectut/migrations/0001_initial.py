# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('threadedcomments', '__first__'),
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
            name='FluentComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('activity', models.ForeignKey(to='lectut.Activity')),
                ('threaded_comments', models.ForeignKey(to='threadedcomments.ThreadedComment')),
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
