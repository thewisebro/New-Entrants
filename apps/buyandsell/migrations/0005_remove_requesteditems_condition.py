# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buyandsell', '0004_remove_saleitems_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requesteditems',
            name='condition',
        ),
    ]
