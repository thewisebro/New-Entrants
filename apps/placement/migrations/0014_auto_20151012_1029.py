# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0013_auto_20150912_0345'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResumeStudentMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('resume_name', models.CharField(max_length=44)),
                ('plac_person', models.ForeignKey(to='placement.PlacementPerson', unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='workshopregistration',
            name='reason',
            field=models.CharField(help_text=b'None', max_length=500, null=True, blank=True),
        ),
    ]
