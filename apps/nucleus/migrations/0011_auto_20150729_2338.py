# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0010_auto_20150726_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinfo',
            name='permanent_address',
            field=models.CharField(max_length=250, verbose_name=b'Permanent Address', blank=True),
        ),
    ]
