# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0011_auto_20150729_2338'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('grade_pay', models.IntegerField(null=True, blank=True)),
                ('acc_no', models.IntegerField(null=True, blank=True)),
                ('phone_office', models.IntegerField(null=True, blank=True)),
                ('phone_resi', models.IntegerField(null=True, blank=True)),
                ('annual_income', models.IntegerField(null=True, blank=True)),
                ('height', models.IntegerField(null=True, blank=True)),
                ('weight', models.IntegerField(null=True, blank=True)),
                ('age', models.IntegerField(null=True, blank=True)),
                ('nominee_name', models.CharField(max_length=20, null=True, blank=True)),
                ('relation_nominee', models.CharField(max_length=20, null=True, blank=True)),
                ('date_of_join_position', core.models.fields.DateTimeField(auto_now=True, max_length=20, null=True)),
                ('week_pref1', models.CharField(blank=True, max_length=20, null=True, choices=[(b'MCM', b'Merit-Cum-Means Scholarship'), (b'GIS', b'Grant of Institute Scholarship(SC/ST)')])),
                ('week_pref2', models.CharField(blank=True, max_length=20, null=True, choices=[(b'MCM', b'Merit-Cum-Means Scholarship'), (b'GIS', b'Grant of Institute Scholarship(SC/ST)')])),
                ('city_pref1', models.CharField(blank=True, max_length=20, null=True, choices=[(b'SCHOL', b'For Scholarship of Rs. 1000/- per month for 10 months'), (b'MESS', b'Free Messing (basic menu only) with Rs. 250/- per month for ten months, as per allowance')])),
                ('city_pref2', models.CharField(blank=True, max_length=20, null=True, choices=[(b'SCHOL', b'For Scholarship of Rs. 1000/- per month for 10 months'), (b'MESS', b'Free Messing (basic menu only) with Rs. 250/- per month for ten months, as per allowance')])),
                ('city_pref3', models.CharField(blank=True, max_length=20, null=True, choices=[(b'SCHOL', b'For Scholarship of Rs. 1000/- per month for 10 months'), (b'MESS', b'Free Messing (basic menu only) with Rs. 250/- per month for ten months, as per allowance')])),
                ('city_pref4', models.CharField(blank=True, max_length=20, null=True, choices=[(b'SCHOL', b'For Scholarship of Rs. 1000/- per month for 10 months'), (b'MESS', b'Free Messing (basic menu only) with Rs. 250/- per month for ten months, as per allowance')])),
                ('city_pref5', models.CharField(blank=True, max_length=20, null=True, choices=[(b'SCHOL', b'For Scholarship of Rs. 1000/- per month for 10 months'), (b'MESS', b'Free Messing (basic menu only) with Rs. 250/- per month for ten months, as per allowance')])),
                ('city_pref6', models.CharField(blank=True, max_length=20, null=True, choices=[(b'SCHOL', b'For Scholarship of Rs. 1000/- per month for 10 months'), (b'MESS', b'Free Messing (basic menu only) with Rs. 250/- per month for ten months, as per allowance')])),
                ('prof', models.OneToOneField(to='nucleus.Faculty')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
