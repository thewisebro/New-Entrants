# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0003_auto_20150416_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='datetime_modified',
            field=core.models.fields.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='trashnotice',
            name='datetime_modified',
            field=core.models.fields.DateTimeField(db_index=True),
        ),
    ]
