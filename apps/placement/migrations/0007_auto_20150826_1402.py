# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0006_auto_20150826_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopregistration',
            name='suggestions',
            field=models.CharField(max_length=300, null=True, verbose_name=b'Target Company', blank=True),
        ),
    ]
