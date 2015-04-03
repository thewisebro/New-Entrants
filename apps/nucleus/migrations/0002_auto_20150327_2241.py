# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webmailaccount',
            name='webmail_id',
            field=models.CharField(max_length=20, serialize=False, primary_key=True),
        ),
    ]
