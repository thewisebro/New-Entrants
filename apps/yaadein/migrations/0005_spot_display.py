# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yaadein', '0004_auto_20150401_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='spot',
            name='display',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
