# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lectut', '0008_auto_20150909_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminders',
            name='event_date',
            field=core.models.fields.DateTimeField(default=datetime.datetime(2015, 10, 4, 18, 59, 59, 626400)),
        ),
    ]
