# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('main_category', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(max_length=100)),
                ('reference', models.CharField(max_length=100, blank=True)),
                ('expire_date', core.models.fields.DateField()),
                ('content', core.models.fields.CKEditorField()),
                ('emailsend', models.BooleanField(default=False)),
                ('re_edited', models.BooleanField(default=False)),
                ('expired_status', models.BooleanField(default=False)),
                ('datetime_modified', core.models.fields.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NoticeUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('subscribed', models.BooleanField(default=False)),
                ('categories', models.ManyToManyField(to='notices.Category')),
                ('read_notices', models.ManyToManyField(related_name=b'read_noticeuser_set', null=True, to='notices.Notice', blank=True)),
                ('starred_notices', models.ManyToManyField(related_name=b'starred_noticeuser_set', null=True, to='notices.Notice', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrashNotice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(max_length=100)),
                ('reference', models.CharField(max_length=100, blank=True)),
                ('expire_date', core.models.fields.DateField()),
                ('content', core.models.fields.CKEditorField()),
                ('emailsend', models.BooleanField(default=False)),
                ('re_edited', models.BooleanField(default=False)),
                ('expired_status', models.BooleanField(default=False)),
                ('datetime_modified', core.models.fields.DateTimeField(auto_now=True)),
                ('notice_id', models.IntegerField()),
                ('editing_no', models.IntegerField()),
                ('original_datetime', core.models.fields.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Uploader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(to='notices.Category')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='trashnotice',
            name='uploader',
            field=models.ForeignKey(to='notices.Uploader'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notice',
            name='uploader',
            field=models.ForeignKey(to='notices.Uploader'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='notices.Uploader'),
            preserve_default=True,
        ),
    ]
