# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bunkometer', '0006_auto_20151101_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='student',
            field=models.ForeignKey(to='nucleus.Student', null=True),
        ),
    ]
