# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0014_auto_20151012_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='contact_no',
            field=models.CharField(max_length=15, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedback',
            name='email',
            field=models.EmailField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='date',
            field=core.models.fields.DateField(),
        ),
    ]
