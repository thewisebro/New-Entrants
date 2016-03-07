# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('messmenu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='bhawan',
            field=models.CharField(max_length=10, choices=[(b'AZB', b'Azad Bhawan'), (b'CTB', b'Cautley Bhawan'), (b'GNB', b'Ganga Bhawan'), (b'GVB', b'Govind Bhawan'), (b'JWB', b'Jawahar Bhawan'), (b'RKB', b'Radhakrishnan Bhawan'), (b'RJB', b'Rajendra Bhawan'), (b'RGB', b'Rajiv Bhawan'), (b'RVB', b'Ravindra Bhawan'), (b'MVB', b'Malviya Bhawan'), (b'SB', b'Sarojini Bhawan'), (b'KB', b'Kasturba Bhawan'), (b'IB', b' Indra Bhawan'), (b'DAY', b'Day Scholar'), (b'KIH', b'Khosla International House')]),
        ),
        migrations.AlterField(
            model_name='menu',
            name='date',
            field=models.DateField(default=datetime.date(2015, 4, 1)),
        ),
    ]
