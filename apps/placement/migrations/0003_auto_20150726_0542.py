# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0002_auto_20150726_0325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campuscontact',
            name='student',
            field=models.ForeignKey(blank=True, to='nucleus.Student', null=True),
        ),
        migrations.AlterField(
            model_name='companycontactcomments',
            name='comment',
            field=models.CharField(max_length=500),
        ),
    ]
