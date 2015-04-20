# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import crop_image.base
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0006_auto_20150417_0353'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('birth_date', core.models.fields.DateField()),
                ('blood_group', models.CharField(max_length=3, verbose_name=b'Blood Group', choices=[(b'O+', b'O+'), (b'O-', b'O-'), (b'AB+', b'AB+'), (b'AB-', b'AB-'), (b'A+', b'A+'), (b'A-', b'A-'), (b'B+', b'B+'), (b'B-', b'B-')])),
                ('personal_contact_no', models.CharField(max_length=12, verbose_name=b'Mobile No. (Self)')),
                ('pincode', models.CharField(max_length=10)),
                ('permanent_address', models.CharField(max_length=100, verbose_name=b'Permanent Address')),
                ('fathers_or_guardians_name', models.CharField(max_length=100, verbose_name=b"Father's /Guardians's Name")),
                ('home_parent_guardian_phone_no', models.CharField(max_length=12, verbose_name=b"Home /Parent's /Local Guardian's Phone No.")),
                ('valid_till', core.models.fields.DateField()),
                ('reason', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pic',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('person', models.OneToOneField(primary_key=True, serialize=False, to='nucleus.Student')),
                ('pic', crop_image.base.CropImageModelField(null=True, upload_to=b'genform/pics/', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='libform',
            name='person',
            field=models.OneToOneField(to='nucleus.Student'),
            preserve_default=True,
        ),
    ]
