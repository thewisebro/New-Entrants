# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('img_website', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='date',
        ),
        migrations.RemoveField(
            model_name='recentworks',
            name='date',
        ),
        migrations.RemoveField(
            model_name='statuspost',
            name='date',
        ),
    ]
