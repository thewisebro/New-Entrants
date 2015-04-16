# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='subject',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='trashnotice',
            name='subject',
            field=models.CharField(max_length=200),
        ),
    ]
