# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0002_auto_20150327_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='bhawan',
            field=models.CharField(default=None, max_length=10, null=True, blank=True, choices=[(b'AZB', b'Azad Bhawan'), (b'CTB', b'Cautley Bhawan'), (b'GNB', b'Ganga Bhawan'), (b'GVB', b'Govind Bhawan'), (b'JWB', b'Jawahar Bhawan'), (b'RKB', b'Radhakrishnan Bhawan'), (b'RJB', b'Rajendra Bhawan'), (b'RGB', b'Rajiv Bhawan'), (b'RVB', b'Ravindra Bhawan'), (b'MVB', b'Malviya Bhawan'), (b'SB', b'Sarojini Bhawan'), (b'KB', b'Kasturba Bhawan'), (b'IB', b' Indra Bhawan'), (b'DAY', b'Day Scholar'), (b'KIH', b'Khosla International House')]),
        ),
    ]
