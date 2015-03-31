# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0002_auto_20150327_2241'),
        ('lectut', '0003_auto_20150323_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='course',
            field=models.ForeignKey(default= 'EE-201:2015', to='nucleus.Course'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='batch',
            field=models.ForeignKey(to='nucleus.Batch', null=True),
        ),
        migrations.AlterField(
            model_name='reminders',
            name='event_date',
            field=core.models.fields.DateTimeField(default=datetime.datetime(2015, 4, 3, 23, 0, 5, 91528)),
        ),
    ]
