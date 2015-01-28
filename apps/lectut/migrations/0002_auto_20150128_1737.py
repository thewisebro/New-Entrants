# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lectut', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fluentcomments',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='fluentcomments',
            name='threaded_comments',
        ),
        migrations.DeleteModel(
            name='FluentComments',
        ),
    ]
