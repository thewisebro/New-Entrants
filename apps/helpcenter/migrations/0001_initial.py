# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('by_img', models.BooleanField(default=False)),
                ('number', models.IntegerField()),
                ('text', models.TextField()),
            ],
            options={
                'ordering': ['number'],
                'verbose_name_plural': 'Replies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
                ('app', models.CharField(max_length=15, blank=True)),
                ('response_type', models.CharField(max_length=10, choices=[(b'feedback', b'Feedback'), (b'help', b'Help')])),
                ('resolved', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=75, blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='reply',
            name='response',
            field=models.ForeignKey(to='helpcenter.Response'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reply',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
