# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0013_auto_20150926_2204'),
        ('bunkometer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='student',
            field=models.ForeignKey(to='nucleus.Student', null=True),
            preserve_default=True,
        ),
    ]
