# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import crop_image.base
import nucleus.models


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0012_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=crop_image.base.CropImageModelField(null=True, upload_to=nucleus.models.user_photo_upload, blank=True),
        ),
    ]
