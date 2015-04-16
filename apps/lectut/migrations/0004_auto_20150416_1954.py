# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import core.models.fields
import lectut.models


class Migration(migrations.Migration):

    dependencies = [
        ('lectut', '0003_auto_20150415_0412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminders',
            name='event_date',
            field=core.models.fields.DateTimeField(default=datetime.datetime(2015, 4, 23, 19, 54, 26, 395541)),
        ),
        migrations.AlterField(
            model_name='uploadedfile',
            name='upload_file',
            field=models.FileField(max_length=250, upload_to=lectut.models.upload_path),
        ),
    ]
