# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mcm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mcmperson',
            name='other_scholarship',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mcmperson',
            name='unfair_means',
            field=models.BooleanField(default=False),
        ),
    ]
