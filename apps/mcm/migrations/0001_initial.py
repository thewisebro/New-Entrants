# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MCM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('scholar_type', models.CharField(blank=True, max_length=10, null=True, choices=[(b'MCM', b'Merit-Cum-Means Scholarship'), (b'GIS', b'Grant of Institute Scholarship(SC/ST)')])),
                ('check', models.BooleanField(default=False)),
                ('air', models.IntegerField(null=True, blank=True)),
                ('unfair_means', models.BooleanField(default=False)),
                ('cgpa', models.CharField(max_length=6, null=True, blank=True)),
                ('sgpa', models.CharField(max_length=6, null=True, blank=True)),
                ('family_income', models.IntegerField(null=True, blank=True)),
                ('other_scholarship_details', models.CharField(max_length=100, null=True, blank=True)),
                ('datetime', core.models.fields.DateTimeField(auto_now=True, null=True)),
                ('payment_choice', models.CharField(blank=True, max_length=10, null=True, choices=[(b'SCHOL', b'For Scholarship of Rs. 1000/- per month for 10 months'), (b'MESS', b'Free Messing (basic menu only) with Rs. 250/- per month for ten months, as per allowance')])),
                ('student', models.OneToOneField(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='McmPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('air', models.IntegerField()),
                ('unfair_means', models.BooleanField()),
                ('family_income', models.IntegerField()),
                ('other_scholarship', models.BooleanField()),
                ('date_time', core.models.fields.DateTimeField()),
                ('student', models.ForeignKey(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StudentLoanAid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('check', models.BooleanField(default=False)),
                ('cgpa', models.CharField(max_length=6, null=True, blank=True)),
                ('sgpa', models.CharField(max_length=6, null=True, blank=True)),
                ('fathers_income', models.IntegerField(null=True, blank=True)),
                ('fathers_pan_no', models.CharField(max_length=10, null=True, blank=True)),
                ('mothers_pan_no', models.CharField(max_length=10, null=True, blank=True)),
                ('gaurdians_pan_no', models.CharField(max_length=10, null=True, blank=True)),
                ('guardians_name', models.CharField(max_length=20, null=True, blank=True)),
                ('guardians_occupation', models.CharField(max_length=20, null=True, blank=True)),
                ('guardians_income', models.IntegerField(null=True, blank=True)),
                ('guardians_address', models.CharField(max_length=50, null=True, blank=True)),
                ('mothers_occupation', models.CharField(max_length=50, null=True, blank=True)),
                ('mothers_income', models.IntegerField(null=True, blank=True)),
                ('other_scholarship_details', models.CharField(max_length=100, null=True, blank=True)),
                ('previous_aid_amount', models.IntegerField(null=True, blank=True)),
                ('previous_aid_session', models.CharField(max_length=9, null=True, blank=True)),
                ('work_bhawan_details', models.CharField(max_length=50, null=True, blank=True)),
                ('date_time', core.models.fields.DateTimeField(null=True, blank=True)),
                ('student', models.OneToOneField(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
