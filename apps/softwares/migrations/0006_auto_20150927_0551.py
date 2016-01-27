# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('softwares', '0005_auto_20150725_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='software',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 27, 5, 51, 46, 401480), verbose_name=b'Date Added'),
        ),
    ]
