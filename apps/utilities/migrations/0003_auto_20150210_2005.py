# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('utilities', '0002_auto_20150210_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useremail',
            name='last_datetime_created',
            field=core.models.fields.DateTimeField(blank=True),
        ),
    ]
