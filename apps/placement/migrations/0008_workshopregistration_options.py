# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0007_auto_20150826_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshopregistration',
            name='options',
            field=models.CharField(default='Group Discussion', max_length=16, choices=[(b'Group Discussion', b'Group Discussion'), (b'Case Study', b'Case Study'), (b'Both', b'Both')]),
            preserve_default=False,
        ),
    ]
