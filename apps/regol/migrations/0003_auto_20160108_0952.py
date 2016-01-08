# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('regol', '0002_auto_20150613_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeredcourses',
            name='year',
            field=models.IntegerField(default=2016),
        ),
    ]
