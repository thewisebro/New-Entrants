# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yaadein', '0003_spot_tagline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(default=b'A', max_length=200, choices=[(b'A', b'Public'), (b'B', b'Private'), (b'D', b'Deleted')]),
        ),
    ]
