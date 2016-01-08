# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0017_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='accepted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='companyapplicationmap',
            name='status',
            field=models.CharField(max_length=3, choices=[(b'APP', b'Applied'), (b'FIN', b'Finalized'), (b'SEL', b'Selected'), (b'ACC', b'Accepted')]),
        ),
    ]
