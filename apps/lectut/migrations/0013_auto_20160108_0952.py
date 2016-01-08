# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lectut', '0012_auto_20150929_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminders',
            name='event_date',
            field=core.models.fields.DateTimeField(default=datetime.datetime(2016, 1, 15, 9, 52, 27, 700758)),
        ),
    ]
