# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buyandsell', '0003_auto_20150909_1246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saleitems',
            name='status',
        ),
    ]
