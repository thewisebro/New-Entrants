# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0015_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('saved', models.BooleanField(default=False)),
                ('declaration', models.BooleanField(default=False)),
                ('grade_pay', models.IntegerField(null=True, blank=True)),
                ('pay_band_basic', models.IntegerField(null=True, blank=True)),
                ('mobile_no', models.CharField(max_length=10, null=True, blank=True)),
                ('phone_office', models.CharField(max_length=20, null=True, blank=True)),
                ('phone_resi', models.CharField(max_length=20, null=True, blank=True)),
                ('annual_income', models.IntegerField(null=True, blank=True)),
                ('height', models.IntegerField(null=True, blank=True)),
                ('weight', models.IntegerField(null=True, blank=True)),
                ('age', models.IntegerField(null=True, blank=True)),
                ('nominee_name', models.CharField(max_length=20, null=True, blank=True)),
                ('relation_nominee', models.CharField(max_length=20, null=True, blank=True)),
                ('date_of_join_position', models.CharField(max_length=20, null=True, blank=True)),
                ('week_pref1', models.CharField(blank=True, max_length=50, null=True, choices=[(b'None', b'None'), (b'WEEK1', b'January 30-31, 2016'), (b'WEEK2', b'February 06-07, 2016')])),
                ('week_pref2', models.CharField(blank=True, max_length=50, null=True, choices=[(b'None', b'None'), (b'WEEK1', b'January 30-31, 2016'), (b'WEEK2', b'February 06-07, 2016')])),
                ('city_pref1', models.CharField(blank=True, max_length=50, null=True, choices=[(b'None', b'None'), (b'Any Exam City', b'Any Exam City '), (b'Amritsar', b'Amritsar'), (b'Ambala', b'Ambala'), (b'Bathinda', b'Bathinda'), (b'Chandigarh-Mohali-Fatehgarh Sahib', b'Chandigarh-Mohali-Fatehgarh Sahib'), (b'Dehradun', b'Dehradun'), (b'Ghaziabad', b'Ghaziabad'), (b'Haldwani-Bhimtal', b'Haldwani-Bhimtal'), (b'Hamirpur (HP)-Una', b'Hamirpur (HP)-Una'), (b'Jalandhar-Phagwara', b'Jalandhar-Phagwara'), (b'Kurukshetra', b'Kurukshetra'), (b'Ludhiana-Moga', b'Ludhiana-Moga'), (b'Meerut', b'Meerut'), (b'Moradabad', b'Moradabad'), (b'Noida', b'Noida'), (b'Panipat', b'Panipat'), (b'Pathankot', b'Pathankot'), (b'Patiala-Sangrur', b'Patiala-Sangrur'), (b'Roorkee-Muzaffarnagar', b'Roorkee-Muzaffarnagar'), (b'Solan-Shimla', b'Solan-Shimla'), (b'Sirmaur', b'Sirmaur'), (b'Sonipat', b'Sonipat'), (b'Yamunanagar', b'Yamunanagar')])),
                ('city_pref2', models.CharField(blank=True, max_length=50, null=True, choices=[(b'None', b'None'), (b'Any Exam City', b'Any Exam City '), (b'Amritsar', b'Amritsar'), (b'Ambala', b'Ambala'), (b'Bathinda', b'Bathinda'), (b'Chandigarh-Mohali-Fatehgarh Sahib', b'Chandigarh-Mohali-Fatehgarh Sahib'), (b'Dehradun', b'Dehradun'), (b'Ghaziabad', b'Ghaziabad'), (b'Haldwani-Bhimtal', b'Haldwani-Bhimtal'), (b'Hamirpur (HP)-Una', b'Hamirpur (HP)-Una'), (b'Jalandhar-Phagwara', b'Jalandhar-Phagwara'), (b'Kurukshetra', b'Kurukshetra'), (b'Ludhiana-Moga', b'Ludhiana-Moga'), (b'Meerut', b'Meerut'), (b'Moradabad', b'Moradabad'), (b'Noida', b'Noida'), (b'Panipat', b'Panipat'), (b'Pathankot', b'Pathankot'), (b'Patiala-Sangrur', b'Patiala-Sangrur'), (b'Roorkee-Muzaffarnagar', b'Roorkee-Muzaffarnagar'), (b'Solan-Shimla', b'Solan-Shimla'), (b'Sirmaur', b'Sirmaur'), (b'Sonipat', b'Sonipat'), (b'Yamunanagar', b'Yamunanagar')])),
                ('city_pref3', models.CharField(blank=True, max_length=50, null=True, choices=[(b'None', b'None'), (b'Any Exam City', b'Any Exam City '), (b'Amritsar', b'Amritsar'), (b'Ambala', b'Ambala'), (b'Bathinda', b'Bathinda'), (b'Chandigarh-Mohali-Fatehgarh Sahib', b'Chandigarh-Mohali-Fatehgarh Sahib'), (b'Dehradun', b'Dehradun'), (b'Ghaziabad', b'Ghaziabad'), (b'Haldwani-Bhimtal', b'Haldwani-Bhimtal'), (b'Hamirpur (HP)-Una', b'Hamirpur (HP)-Una'), (b'Jalandhar-Phagwara', b'Jalandhar-Phagwara'), (b'Kurukshetra', b'Kurukshetra'), (b'Ludhiana-Moga', b'Ludhiana-Moga'), (b'Meerut', b'Meerut'), (b'Moradabad', b'Moradabad'), (b'Noida', b'Noida'), (b'Panipat', b'Panipat'), (b'Pathankot', b'Pathankot'), (b'Patiala-Sangrur', b'Patiala-Sangrur'), (b'Roorkee-Muzaffarnagar', b'Roorkee-Muzaffarnagar'), (b'Solan-Shimla', b'Solan-Shimla'), (b'Sirmaur', b'Sirmaur'), (b'Sonipat', b'Sonipat'), (b'Yamunanagar', b'Yamunanagar')])),
                ('city_pref4', models.CharField(blank=True, max_length=50, null=True, choices=[(b'None', b'None'), (b'Any Exam City', b'Any Exam City '), (b'Amritsar', b'Amritsar'), (b'Ambala', b'Ambala'), (b'Bathinda', b'Bathinda'), (b'Chandigarh-Mohali-Fatehgarh Sahib', b'Chandigarh-Mohali-Fatehgarh Sahib'), (b'Dehradun', b'Dehradun'), (b'Ghaziabad', b'Ghaziabad'), (b'Haldwani-Bhimtal', b'Haldwani-Bhimtal'), (b'Hamirpur (HP)-Una', b'Hamirpur (HP)-Una'), (b'Jalandhar-Phagwara', b'Jalandhar-Phagwara'), (b'Kurukshetra', b'Kurukshetra'), (b'Ludhiana-Moga', b'Ludhiana-Moga'), (b'Meerut', b'Meerut'), (b'Moradabad', b'Moradabad'), (b'Noida', b'Noida'), (b'Panipat', b'Panipat'), (b'Pathankot', b'Pathankot'), (b'Patiala-Sangrur', b'Patiala-Sangrur'), (b'Roorkee-Muzaffarnagar', b'Roorkee-Muzaffarnagar'), (b'Solan-Shimla', b'Solan-Shimla'), (b'Sirmaur', b'Sirmaur'), (b'Sonipat', b'Sonipat'), (b'Yamunanagar', b'Yamunanagar')])),
                ('city_pref5', models.CharField(blank=True, max_length=50, null=True, choices=[(b'None', b'None'), (b'Any Exam City', b'Any Exam City '), (b'Amritsar', b'Amritsar'), (b'Ambala', b'Ambala'), (b'Bathinda', b'Bathinda'), (b'Chandigarh-Mohali-Fatehgarh Sahib', b'Chandigarh-Mohali-Fatehgarh Sahib'), (b'Dehradun', b'Dehradun'), (b'Ghaziabad', b'Ghaziabad'), (b'Haldwani-Bhimtal', b'Haldwani-Bhimtal'), (b'Hamirpur (HP)-Una', b'Hamirpur (HP)-Una'), (b'Jalandhar-Phagwara', b'Jalandhar-Phagwara'), (b'Kurukshetra', b'Kurukshetra'), (b'Ludhiana-Moga', b'Ludhiana-Moga'), (b'Meerut', b'Meerut'), (b'Moradabad', b'Moradabad'), (b'Noida', b'Noida'), (b'Panipat', b'Panipat'), (b'Pathankot', b'Pathankot'), (b'Patiala-Sangrur', b'Patiala-Sangrur'), (b'Roorkee-Muzaffarnagar', b'Roorkee-Muzaffarnagar'), (b'Solan-Shimla', b'Solan-Shimla'), (b'Sirmaur', b'Sirmaur'), (b'Sonipat', b'Sonipat'), (b'Yamunanagar', b'Yamunanagar')])),
                ('city_pref6', models.CharField(blank=True, max_length=50, null=True, choices=[(b'None', b'None'), (b'Any Exam City', b'Any Exam City '), (b'Amritsar', b'Amritsar'), (b'Ambala', b'Ambala'), (b'Bathinda', b'Bathinda'), (b'Chandigarh-Mohali-Fatehgarh Sahib', b'Chandigarh-Mohali-Fatehgarh Sahib'), (b'Dehradun', b'Dehradun'), (b'Ghaziabad', b'Ghaziabad'), (b'Haldwani-Bhimtal', b'Haldwani-Bhimtal'), (b'Hamirpur (HP)-Una', b'Hamirpur (HP)-Una'), (b'Jalandhar-Phagwara', b'Jalandhar-Phagwara'), (b'Kurukshetra', b'Kurukshetra'), (b'Ludhiana-Moga', b'Ludhiana-Moga'), (b'Meerut', b'Meerut'), (b'Moradabad', b'Moradabad'), (b'Noida', b'Noida'), (b'Panipat', b'Panipat'), (b'Pathankot', b'Pathankot'), (b'Patiala-Sangrur', b'Patiala-Sangrur'), (b'Roorkee-Muzaffarnagar', b'Roorkee-Muzaffarnagar'), (b'Solan-Shimla', b'Solan-Shimla'), (b'Sirmaur', b'Sirmaur'), (b'Sonipat', b'Sonipat'), (b'Yamunanagar', b'Yamunanagar')])),
                ('prof', models.OneToOneField(to='nucleus.Faculty')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
