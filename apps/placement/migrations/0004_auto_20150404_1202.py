# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0003_auto_20150217_2326'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='category_required',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='placementperson',
            name='photo',
            field=core.models.fields.AutoDeleteImageField(help_text=b"<span style='font-size:0.9em;'>Recommended size: <b>35mm width x 45mm height</b></span>", null=True, upload_to=b'placement/photos/', blank=True),
        ),
    ]
