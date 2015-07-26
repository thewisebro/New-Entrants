# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0005_auto_20150330_1757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companycontactinfo',
            name='primary_contact_person',
        ),
        migrations.AddField(
            model_name='contactperson',
            name='is_primary',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
