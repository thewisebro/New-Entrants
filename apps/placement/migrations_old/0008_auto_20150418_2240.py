# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0007_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companycontactinfo',
            name='name',
            field=models.CharField(unique=True, max_length=250),
        ),
    ]
