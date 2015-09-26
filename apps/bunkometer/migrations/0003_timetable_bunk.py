# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bunkometer', '0002_auto_20150913_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='bunk',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
