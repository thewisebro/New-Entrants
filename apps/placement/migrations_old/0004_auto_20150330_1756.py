# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0003_auto_20150217_2326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companycontact',
            name='contactperson',
        ),
        migrations.RemoveField(
            model_name='companycoordi',
            name='student',
        ),
        migrations.DeleteModel(
            name='CompanyCoordi',
        ),
        migrations.DeleteModel(
            name='ContactPerson',
        ),
        migrations.RemoveField(
            model_name='placementmgr',
            name='company_name',
        ),
        migrations.DeleteModel(
            name='CompanyContact',
        ),
        migrations.RemoveField(
            model_name='placementmgr',
            name='coordi',
        ),
        migrations.DeleteModel(
            name='PlacementMgr',
        ),
    ]
