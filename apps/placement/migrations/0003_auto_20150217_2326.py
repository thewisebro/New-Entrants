# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0002_auto_20150121_0036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facebook',
            name='student',
        ),
        migrations.DeleteModel(
            name='Facebook',
        ),
    ]
