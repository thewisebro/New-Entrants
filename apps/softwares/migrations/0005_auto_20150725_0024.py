# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('softwares', '0004_auto_20150725_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='software',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 25, 0, 24, 42, 294348), verbose_name=b'Date Added'),
        ),
    ]
