# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buyandsell', '0002_auto_20150909_1136'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pic',
            new_name='ItemPic',
        ),
    ]
