# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit_autocomplete.managers
import core.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nucleus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('text_content', models.CharField(max_length=200)),
                ('upvote', models.IntegerField()),
                ('post_date', core.models.fields.DateTimeField(auto_now=True)),
                ('status', models.CharField(default=b'A', max_length=200, choices=[(b'A', b'Public'), (b'B', b'Private'), (b'RA', b'Report Abuse')])),
                ('owner', models.ForeignKey(related_name=b'post_owner', to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('image', models.FileField(upload_to=b'yaadein/')),
                ('post', models.ForeignKey(to='yaadein.Post')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Spot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('profile_pic', models.FileField(null=True, upload_to=b'yaadein/spot/', blank=True)),
                ('coverpic', models.FileField(null=True, upload_to=b'yaadein/coverpic/', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='YaadeinUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('coverpic', models.FileField(null=True, upload_to=b'yaadein/coverpic/', blank=True)),
                ('status', models.CharField(default=b'A', max_length=200, choices=[(b'A', b'Active'), (b'B', b'Blocked')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='spots',
            field=models.ManyToManyField(to='yaadein.Spot'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=taggit_autocomplete.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='user_tags',
            field=models.ManyToManyField(related_name=b'tagged_user', to='nucleus.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='wall_user',
            field=models.ForeignKey(related_name=b'post_wall_user', to='nucleus.Student'),
            preserve_default=True,
        ),
    ]
