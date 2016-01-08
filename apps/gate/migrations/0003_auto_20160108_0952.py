# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gate', '0002_auto_20150909_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gate',
            name='acc_no',
        ),
        migrations.AddField(
            model_name='gate',
            name='declaration',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gate',
            name='mobile_no',
            field=models.CharField(max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gate',
            name='pay_band_basic',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gate',
            name='saved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gate',
            name='city_pref1',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'None', b'None'), (b'Any Exam City', b'Any Exam City '), (b'Amritsar', b'Amritsar'), (b'Ambala', b'Ambala'), (b'Bathinda', b'Bathinda'), (b'Chandigarh-Mohali-Fatehgarh Sahib', b'Chandigarh-Mohali-Fatehgarh Sahib'), (b'Dehradun', b'Dehradun'), (b'Ghaziabad', b'Ghaziabad'), (b'Haldwani-Bhimtal', b'Haldwani-Bhimtal'), (b'Hamirpur (HP)-Una', b'Hamirpur (HP)-Una'), (b'Jalandhar-Phagwara', b'Jalandhar-Phagwara'), (b'Kurukshetra', b'Kurukshetra'), (b'Ludhiana-Moga', b'Ludhiana-Moga'), (b'Meerut', b'Meerut'), (b'Moradabad', b'Moradabad'), (b'Noida', b'Noida'), (b'Panipat', b'Panipat'), (b'Pathankot', b'Pathankot'), (b'Patiala-Sangrur', b'Patiala-Sangrur'), (b'Roorkee-Muzaffarnagar', b'Roorkee-Muzaffarnagar'), (b'Solan-Shimla', b'Solan-Shimla'), (b'Sirmaur', b'Sirmaur'), (b'Sonipat', b'Sonipat'), (b'Yamunanagar', b'Yamunanagar')]),
        ),
        migrations.AlterField(
            model_name='gate',
            name='city_pref2',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'None', b'None'), (b'Any Exam City', b'Any Exam City '), (b'Amritsar', b'Amritsar'), (b'Ambala', b'Ambala'), (b'Bathinda', b'Bathinda'), (b'Chandigarh-Mohali-Fatehgarh Sahib', b'Chandigarh-Mohali-Fatehgarh Sahib'), (b'Dehradun', b'Dehradun'), (b'Ghaziabad', b'Ghaziabad'), (b'Haldwani-Bhimtal', b'Haldwani-Bhimtal'), (b'Hamirpur (HP)-Una', b'Hamirpur (HP)-Una'), (b'Jalandhar-Phagwara', b'Jalandhar-Phagwara'), (b'Kurukshetra', b'Kurukshetra'), (b'Ludhiana-Moga', b'Ludhiana-Moga'), (b'Meerut', b'Meerut'), (b'Moradabad', b'Moradabad'), (b'Noida', b'Noida'), (b'Panipat', b'Panipat'), (b'Pathankot', b'Pathankot'), (b'Patiala-Sangrur', b'Patiala-Sangrur'), (b'Roorkee-Muzaffarnagar', b'Roorkee-Muzaffarnagar'), (b'Solan-Shimla', b'Solan-Shimla'), (b'Sirmaur', b'Sirmaur'), (b'Sonipat', b'Sonipat'), (b'Yamunanagar', b'Yamunanagar')]),
        ),
        migrations.AlterField(
            model_name='gate',
            name='city_pref3',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'None', b'None'), (b'Any Exam City', b'Any Exam City '), (b'Amritsar', b'Amritsar'), (b'Ambala', b'Ambala'), (b'Bathinda', b'Bathinda'), (b'Chandigarh-Mohali-Fatehgarh Sahib', b'Chandigarh-Mohali-Fatehgarh Sahib'), (b'Dehradun', b'Dehradun'), (b'Ghaziabad', b'Ghaziabad'), (b'Haldwani-Bhimtal', b'Haldwani-Bhimtal'), (b'Hamirpur (HP)-Una', b'Hamirpur (HP)-Una'), (b'Jalandhar-Phagwara', b'Jalandhar-Phagwara'), (b'Kurukshetra', b'Kurukshetra'), (b'Ludhiana-Moga', b'Ludhiana-Moga'), (b'Meerut', b'Meerut'), (b'Moradabad', b'Moradabad'), (b'Noida', b'Noida'), (b'Panipat', b'Panipat'), (b'Pathankot', b'Pathankot'), (b'Patiala-Sangrur', b'Patiala-Sangrur'), (b'Roorkee-Muzaffarnagar', b'Roorkee-Muzaffarnagar'), (b'Solan-Shimla', b'Solan-Shimla'), (b'Sirmaur', b'Sirmaur'), (b'Sonipat', b'Sonipat'), (b'Yamunanagar', b'Yamunanagar')]),
        ),
        migrations.AlterField(
            model_name='gate',
            name='city_pref4',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'None', b'None'), (b'Any Exam City', b'Any Exam City '), (b'Amritsar', b'Amritsar'), (b'Ambala', b'Ambala'), (b'Bathinda', b'Bathinda'), (b'Chandigarh-Mohali-Fatehgarh Sahib', b'Chandigarh-Mohali-Fatehgarh Sahib'), (b'Dehradun', b'Dehradun'), (b'Ghaziabad', b'Ghaziabad'), (b'Haldwani-Bhimtal', b'Haldwani-Bhimtal'), (b'Hamirpur (HP)-Una', b'Hamirpur (HP)-Una'), (b'Jalandhar-Phagwara', b'Jalandhar-Phagwara'), (b'Kurukshetra', b'Kurukshetra'), (b'Ludhiana-Moga', b'Ludhiana-Moga'), (b'Meerut', b'Meerut'), (b'Moradabad', b'Moradabad'), (b'Noida', b'Noida'), (b'Panipat', b'Panipat'), (b'Pathankot', b'Pathankot'), (b'Patiala-Sangrur', b'Patiala-Sangrur'), (b'Roorkee-Muzaffarnagar', b'Roorkee-Muzaffarnagar'), (b'Solan-Shimla', b'Solan-Shimla'), (b'Sirmaur', b'Sirmaur'), (b'Sonipat', b'Sonipat'), (b'Yamunanagar', b'Yamunanagar')]),
        ),
        migrations.AlterField(
            model_name='gate',
            name='city_pref5',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'None', b'None'), (b'Any Exam City', b'Any Exam City '), (b'Amritsar', b'Amritsar'), (b'Ambala', b'Ambala'), (b'Bathinda', b'Bathinda'), (b'Chandigarh-Mohali-Fatehgarh Sahib', b'Chandigarh-Mohali-Fatehgarh Sahib'), (b'Dehradun', b'Dehradun'), (b'Ghaziabad', b'Ghaziabad'), (b'Haldwani-Bhimtal', b'Haldwani-Bhimtal'), (b'Hamirpur (HP)-Una', b'Hamirpur (HP)-Una'), (b'Jalandhar-Phagwara', b'Jalandhar-Phagwara'), (b'Kurukshetra', b'Kurukshetra'), (b'Ludhiana-Moga', b'Ludhiana-Moga'), (b'Meerut', b'Meerut'), (b'Moradabad', b'Moradabad'), (b'Noida', b'Noida'), (b'Panipat', b'Panipat'), (b'Pathankot', b'Pathankot'), (b'Patiala-Sangrur', b'Patiala-Sangrur'), (b'Roorkee-Muzaffarnagar', b'Roorkee-Muzaffarnagar'), (b'Solan-Shimla', b'Solan-Shimla'), (b'Sirmaur', b'Sirmaur'), (b'Sonipat', b'Sonipat'), (b'Yamunanagar', b'Yamunanagar')]),
        ),
        migrations.AlterField(
            model_name='gate',
            name='city_pref6',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'None', b'None'), (b'Any Exam City', b'Any Exam City '), (b'Amritsar', b'Amritsar'), (b'Ambala', b'Ambala'), (b'Bathinda', b'Bathinda'), (b'Chandigarh-Mohali-Fatehgarh Sahib', b'Chandigarh-Mohali-Fatehgarh Sahib'), (b'Dehradun', b'Dehradun'), (b'Ghaziabad', b'Ghaziabad'), (b'Haldwani-Bhimtal', b'Haldwani-Bhimtal'), (b'Hamirpur (HP)-Una', b'Hamirpur (HP)-Una'), (b'Jalandhar-Phagwara', b'Jalandhar-Phagwara'), (b'Kurukshetra', b'Kurukshetra'), (b'Ludhiana-Moga', b'Ludhiana-Moga'), (b'Meerut', b'Meerut'), (b'Moradabad', b'Moradabad'), (b'Noida', b'Noida'), (b'Panipat', b'Panipat'), (b'Pathankot', b'Pathankot'), (b'Patiala-Sangrur', b'Patiala-Sangrur'), (b'Roorkee-Muzaffarnagar', b'Roorkee-Muzaffarnagar'), (b'Solan-Shimla', b'Solan-Shimla'), (b'Sirmaur', b'Sirmaur'), (b'Sonipat', b'Sonipat'), (b'Yamunanagar', b'Yamunanagar')]),
        ),
        migrations.AlterField(
            model_name='gate',
            name='date_of_join_position',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='gate',
            name='phone_office',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='gate',
            name='phone_resi',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='gate',
            name='week_pref1',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'None', b'None'), (b'WEEK1', b'January 30-31, 2016'), (b'WEEK2', b'February 06-07, 2016')]),
        ),
        migrations.AlterField(
            model_name='gate',
            name='week_pref2',
            field=models.CharField(blank=True, max_length=50, null=True, choices=[(b'None', b'None'), (b'WEEK1', b'January 30-31, 2016'), (b'WEEK2', b'February 06-07, 2016')]),
        ),
    ]
