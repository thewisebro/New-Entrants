# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yaadein', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='spot',
            name='name',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='upvote',
            field=models.IntegerField(default=0),
        ),
    ]
