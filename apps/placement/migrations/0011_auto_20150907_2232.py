# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0010_auto_20150901_2028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshoppriority',
            name='student',
        ),
        migrations.DeleteModel(
            name='WorkshopPriority',
        ),
        migrations.RemoveField(
            model_name='workshopregistration',
            name='is_registered',
        ),
        migrations.RemoveField(
            model_name='workshopregistration',
            name='suggestions',
        ),
        migrations.AddField(
            model_name='workshopregistration',
            name='reason',
            field=models.CharField(max_length=500, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workshopregistration',
            name='options',
            field=models.CharField(default=b'NOT', max_length=16, choices=[(b'Smart India', b'Smart India'), (b'4P Education', b'4P Education'), (b'Talerang', b'Talerang'), (b'Ethuns Consultancy Service', b'Ethuns Consultancy Service'), (b'NOT', b'Not interested')]),
        ),
    ]
