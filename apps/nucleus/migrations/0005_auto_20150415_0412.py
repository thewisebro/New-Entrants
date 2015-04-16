# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0004_auto_20150415_0356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='id',
            field=models.CharField(max_length=60, serialize=False, primary_key=True),
        ),
    ]
