# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('messmenu', '0003_auto_20150725_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='date',
            field=models.DateField(default=datetime.date(2015, 9, 9)),
        ),
    ]
