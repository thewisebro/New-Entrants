# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buyandsell', '0005_remove_requesteditems_condition'),
    ]

    operations = [
        migrations.CreateModel(
            name='OldBuyMap',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('buy_id', models.IntegerField(serialize=False, primary_key=True)),
                ('item', models.ForeignKey(to='buyandsell.SaleItems')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OldRequestMap',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('request_id', models.IntegerField(serialize=False, primary_key=True)),
                ('item', models.ForeignKey(to='buyandsell.RequestedItems')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
