# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('softwares', '0003_auto_20150401_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='software',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 25, 0, 11, 57, 642388), verbose_name=b'Date Added'),
        ),
    ]
