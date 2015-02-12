# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import core.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('lectut', '0001_initial'),
    ]
    operations = [
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
    ]
