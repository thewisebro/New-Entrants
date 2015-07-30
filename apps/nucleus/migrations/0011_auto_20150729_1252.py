# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0010_auto_20150726_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinfo',
            name='fathers_office_phone_no',
            field=models.CharField(max_length=20, verbose_name=b"Father's Office Phone No", blank=True),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='home_contact_no',
            field=models.CharField(max_length=20, verbose_name=b'Home Contact No', blank=True),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='local_guardian_contact_no',
            field=models.CharField(max_length=20, verbose_name=b"Local Guardian's Contact No", blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='contact_no',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Contact No', blank=True),
        ),
    ]
