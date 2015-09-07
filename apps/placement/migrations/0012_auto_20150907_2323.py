# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0011_auto_20150907_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopregistration',
            name='options',
            field=models.CharField(default=b'NOT', max_length=28, choices=[(b'NOT', b'Not interested'), (b'Smart India', b'Smart India'), (b'4P Education', b'4P Education'), (b'Talerang', b'Talerang'), (b'Ethuns Consultancy Service', b'Ethuns Consultancy Service')]),
        ),
    ]
