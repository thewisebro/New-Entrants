# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bunkometer', '0002_auto_20150325_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='class_type',
            field=models.CharField(max_length=4),
        ),
    ]
