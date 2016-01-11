# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0015_auto_20151129_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='profile_offered',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
