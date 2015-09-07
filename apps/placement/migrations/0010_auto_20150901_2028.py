# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0009_auto_20150901_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pporejection',
            name='plac_person',
            field=models.ForeignKey(to='placement.PlacementPerson', unique=True),
        ),
    ]
