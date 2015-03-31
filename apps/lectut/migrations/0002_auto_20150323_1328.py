# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lectut', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='deleted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='deleted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reminders',
            name='event_date',
            field=core.models.fields.DateTimeField(default=datetime.datetime(2015, 3, 30, 13, 28, 7, 312267)),
        ),
    ]
