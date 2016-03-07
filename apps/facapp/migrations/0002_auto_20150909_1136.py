# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refereedjournalpapers',
            name='papers',
            field=models.TextField(blank=True),
        ),
    ]
