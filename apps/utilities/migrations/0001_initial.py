# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordCheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('service', models.CharField(max_length=40)),
                ('seconds', models.PositiveIntegerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=255)),
                ('verified', models.BooleanField(default=False)),
                ('confirmation_key', models.CharField(max_length=40, blank=True)),
                ('last_datetime_created', core.models.fields.DateTimeField(null=True, blank=True)),
                ('verify_num', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('session_key', models.CharField(max_length=40)),
                ('ip', models.CharField(max_length=40)),
                ('browser', models.CharField(max_length=40)),
                ('os', models.CharField(max_length=40)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
