# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import crop_image.base


class Migration(migrations.Migration):

    dependencies = [
        ('buyandsell', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pic',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('item', models.OneToOneField(primary_key=True, serialize=False, to='buyandsell.SaleItems')),
                ('pic', crop_image.base.CropImageModelField(null=True, upload_to=b'buyandsell/pics/', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='saleitems',
            name='item_image',
        ),
    ]
