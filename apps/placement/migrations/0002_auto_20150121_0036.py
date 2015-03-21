# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyapplicationmap',
            name='time_of_application',
            field=core.models.fields.DateTimeField(auto_now=True),
        ),
    ]
