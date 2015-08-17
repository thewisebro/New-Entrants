# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('regol', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registeredcourses',
            name='semester_type',
            field=models.CharField(default=b'A', max_length=10),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='registeredcourses',
            name='year',
            field=models.IntegerField(default=2015),
            preserve_default=True,
        ),
    ]
