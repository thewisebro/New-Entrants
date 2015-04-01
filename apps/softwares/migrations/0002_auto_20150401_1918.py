# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('softwares', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='software',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 1, 19, 17, 46, 700820), verbose_name=b'Date Added'),
        ),
    ]
