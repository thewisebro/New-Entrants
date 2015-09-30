# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0008_workshopregistration_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='PpoRejection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('package', models.CharField(max_length=20, null=True, verbose_name=b'Package', blank=True)),
                ('company', models.ForeignKey(to='placement.Company')),
                ('plac_person', models.ForeignKey(to='placement.PlacementPerson')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='workshopregistration',
            name='options',
            field=models.CharField(default=b'Group Discussion', max_length=16, choices=[(b'Group Discussion', b'Group Discussion'), (b'Case Study', b'Case Study'), (b'Both', b'Both')]),
        ),
        migrations.AlterField(
            model_name='workshopregistration',
            name='placement_person',
            field=models.ForeignKey(to='placement.PlacementPerson', unique=True),
        ),
        migrations.AlterField(
            model_name='workshopregistration',
            name='suggestions',
            field=models.CharField(max_length=300, null=True, verbose_name=b'Target Companies', blank=True),
        ),
    ]
