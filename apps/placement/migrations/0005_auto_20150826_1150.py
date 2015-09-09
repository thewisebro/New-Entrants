# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0004_auto_20150826_1053'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workshopregistration',
            old_name='registerd',
            new_name='is_registered',
        ),
    ]
