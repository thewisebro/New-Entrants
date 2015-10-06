# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('softwares', '0007_auto_20150909_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='software',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 27, 18, 59, 59, 749304), verbose_name=b'Date Added'),
        ),
    ]
