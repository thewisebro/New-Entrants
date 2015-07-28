# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0001_initial'),
        ('placement', '0004_auto_20150330_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampusContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('last_contact', models.CharField(max_length=100, null=True, blank=True)),
                ('when_to_contact', core.models.fields.DateField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyContactComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(max_length=300)),
                ('date_created', core.models.fields.DateTimeField(auto_now_add=True)),
                ('campus_contact', models.ForeignKey(to='placement.CampusContact')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyContactInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=250)),
                ('cluster', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)])),
                ('status', models.CharField(blank=True, max_length=40, null=True, choices=[(b'JAF Sent', b'JAF Sent'), (b'JAF Received', b'JAF Received'), (b'STF Sent', b'STF Sent'), (b'Not Called', b'Not Called'), (b'JAF + STF sent', b'JAF + STF sent'), (b'JAF+ STF recieved', b'JAF+ STF recieved'), (b'Not Picking Up', b'Not Picking Up'), (b'Incorrect contact info', b'Incorrect contact info'), (b'Call Later', b'call later'), (b'Denied', b'Denied'), (b'Process Confirmed', b'Process Confirmed'), (b'Other', b'Other')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=250)),
                ('designation', models.CharField(max_length=100, null=True, blank=True)),
                ('phone_no', models.CharField(max_length=250, null=True, blank=True)),
                ('email', models.CharField(max_length=250, null=True, blank=True)),
                ('company_contact', models.ForeignKey(to='placement.CompanyContactInfo')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='companycontactinfo',
            name='primary_contact_person',
            field=models.OneToOneField(to='placement.ContactPerson'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campuscontact',
            name='contact_person',
            field=models.OneToOneField(to='placement.ContactPerson'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campuscontact',
            name='student',
            field=models.ForeignKey(to='nucleus.Student'),
            preserve_default=True,
        ),
    ]
