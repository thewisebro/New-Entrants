# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0012_auto_20150907_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pporejection',
            name='company',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
