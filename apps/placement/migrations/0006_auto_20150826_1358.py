# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0005_auto_20150826_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshopregistration',
            name='suggestions',
            field=models.TextField(null=True, verbose_name=b'Company to be fouces', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workshopregistration',
            name='is_registered',
            field=models.BooleanField(default=False, verbose_name=b'Select to register'),
        ),
    ]
