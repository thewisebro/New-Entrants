# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0003_auto_20150726_0542'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkshopRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('registerd', models.BooleanField(default=False)),
                ('placement_person', models.ForeignKey(to='placement.PlacementPerson')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='researchpublications',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
