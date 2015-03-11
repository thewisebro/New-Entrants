# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nickname', models.CharField(max_length=100)),
                ('website', models.URLField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupInfo',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('group', models.OneToOneField(primary_key=True, serialize=False, to='groups.Group')),
                ('mission', models.TextField(null=True, blank=True)),
                ('founding_year', models.CharField(max_length=100, null=True, blank=True)),
                ('facebook_url', models.URLField(blank=True)),
                ('twitter_url', models.URLField(blank=True)),
                ('gplus_url', models.URLField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('groupinfo', models.ForeignKey(to='groups.GroupInfo')),
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
                ('post_name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='membership',
            name='post',
            field=models.ForeignKey(to='groups.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='membership',
            name='student',
            field=models.ForeignKey(to='nucleus.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupinfo',
            name='members',
            field=models.ManyToManyField(related_name=b'groupinfos', through='groups.Membership', to='nucleus.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupinfo',
            name='posts',
            field=models.ManyToManyField(to='groups.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupinfo',
            name='subscribers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupactivity',
            name='group',
            field=models.ForeignKey(to='groups.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='admin',
            field=models.ForeignKey(related_name=b'student_group_set', blank=True, to='nucleus.Student', null=True),
            preserve_default=True,
        ),
    ]
