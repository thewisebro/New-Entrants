# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('app', models.CharField(max_length=10)),
                ('content', models.TextField(blank=True)),
                ('instance_id', models.PositiveIntegerField(null=True, blank=True)),
                ('link', models.CharField(max_length=200, blank=True)),
                ('dummy', models.BooleanField(default=False)),
                ('last_modified', core.models.fields.DateTimeField(auto_now=True)),
                ('instance_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
                ('shown_feed', models.ForeignKey(related_name=b'dependent_feeds', blank=True, to='feeds.Feed', null=True)),
            ],
            options={
                'ordering': ['-pk'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeedTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('key', models.CharField(max_length=10)),
                ('value', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='feedtag',
            unique_together=set([('key', 'value')]),
        ),
        migrations.AddField(
            model_name='feed',
            name='tags',
            field=models.ManyToManyField(to='feeds.FeedTag', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feed',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
