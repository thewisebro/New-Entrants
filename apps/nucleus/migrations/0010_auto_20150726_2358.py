# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import crop_image.base


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0009_auto_20150726_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='contact_no',
            field=models.CharField(max_length=12, null=True, verbose_name=b'Contact No', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='date joined'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=75, null=True, verbose_name='email address', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'M', b'Male'), (b'F', b'Female')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=crop_image.base.CropImageModelField(null=True, upload_to=b'nucleus/photo/', blank=True),
        ),
    ]
