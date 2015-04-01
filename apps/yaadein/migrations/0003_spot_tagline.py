# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yaadein', '0002_auto_20150318_0138'),
    ]

    operations = [
        migrations.AddField(
            model_name='spot',
            name='tagline',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
    ]
