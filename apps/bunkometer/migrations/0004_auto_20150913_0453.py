# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bunkometer', '0003_timetable_bunk'),
    ]

    operations = [
        migrations.AddField(
            model_name='bunk',
            name='prac_total',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bunk',
            name='tut_total',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
