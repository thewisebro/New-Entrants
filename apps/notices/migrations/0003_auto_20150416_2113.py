# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0002_auto_20150416_0447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='datetime_modified',
            field=core.models.fields.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='notice',
            name='expired_status',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='trashnotice',
            name='datetime_modified',
            field=core.models.fields.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='trashnotice',
            name='expired_status',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
