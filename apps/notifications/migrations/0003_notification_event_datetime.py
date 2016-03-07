# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20150725_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='event_datetime',
            field=core.models.fields.DateTimeField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
