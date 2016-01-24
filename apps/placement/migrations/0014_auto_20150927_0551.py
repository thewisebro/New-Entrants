# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0013_auto_20150912_0345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopregistration',
            name='reason',
            field=models.CharField(help_text=b'None', max_length=500, null=True, blank=True),
        ),
    ]
