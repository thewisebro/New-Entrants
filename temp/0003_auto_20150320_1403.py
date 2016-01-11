# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('buyandsell', '0002_auto_20150212_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='successfultransaction',
            name='buyer',
            field=models.ForeignKey(related_name=b'suc_trans_buyer', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='successfultransaction',
            name='request_item',
            field=models.OneToOneField(null=True, blank=True, to='buyandsell.RequestedItems'),
        ),
        migrations.AlterField(
            model_name='successfultransaction',
            name='sell_item',
            field=models.OneToOneField(null=True, blank=True, to='buyandsell.SaleItems'),
        ),
        migrations.AlterField(
            model_name='successfultransaction',
            name='seller',
            field=models.ForeignKey(related_name=b'suc_trans_seller', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
