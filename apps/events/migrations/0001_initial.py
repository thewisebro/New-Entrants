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
            name='Calendar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('cal_type', models.CharField(max_length=10, choices=[(b'PUB', b'Public'), (b'PRI', b'Private'), (b'GRP', b'Group')])),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('date', core.models.fields.DateField()),
                ('time', core.models.fields.TimeField(null=True, blank=True)),
                ('upto_date', core.models.fields.DateField(null=True, blank=True)),
                ('upto_time', core.models.fields.TimeField(null=True, blank=True)),
                ('place', models.CharField(max_length=100, verbose_name=b'Venue', blank=True)),
                ('description', core.models.fields.CKEditorField(blank=True)),
                ('event_type', models.CharField(max_length=10, choices=[(b'NOEMAIL', b'No Email will be sent to subscribers.'), (b'EMAIL', b'Email will be sent to subscribers within 1 hour of event creation.'), (b'REMINDER', b'A Reminder mail will be sent to subscribers 6 hours before event start.')])),
                ('datetime_added', core.models.fields.DateTimeField(auto_now_add=True)),
                ('email_sent', models.BooleanField(default=False)),
                ('calendar', models.ForeignKey(to='events.Calendar')),
                ('uploader', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date', 'time'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventsUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('email_subscribed', models.BooleanField(default=True)),
                ('calendars', models.ManyToManyField(to='events.Calendar', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
