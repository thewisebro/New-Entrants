# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
#        ('nucleus', '0007_merge'),
        ('placement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampusContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('last_contact', models.CharField(max_length=100, null=True, blank=True)),
                ('when_to_contact', core.models.fields.DateField(null=True, blank=True)),
                ('contact_person', models.OneToOneField(to='placement.ContactPerson')),
                ('student', models.ForeignKey(to='nucleus.Student')),
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
                ('name', models.CharField(help_text=b'Should be unique', unique=True, max_length=250)),
                ('cluster', models.IntegerField(blank=True, null=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)])),
                ('status', models.CharField(blank=True, max_length=40, null=True, choices=[(b'JAF Sent', b'JAF Sent'), (b'JAF Received', b'JAF Received'), (b'STF Sent', b'STF Sent'), (b'Not Called', b'Not Called'), (b'JAF + STF sent', b'JAF + STF sent'), (b'JAF+ STF recieved', b'JAF+ STF recieved'), (b'Not Picking Up', b'Not Picking Up'), (b'Incorrect contact info', b'Incorrect contact info'), (b'Call Later', b'call later'), (b'Denied', b'Denied'), (b'Process Confirmed', b'Process Confirmed'), (b'Other', b'Other')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='contactperson',
            old_name='contact_person',
            new_name='name',
        ),
        migrations.AddField(
            model_name='contactperson',
            name='company_contact',
            field=models.ForeignKey(blank=True, to='placement.CompanyContactInfo', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contactperson',
            name='is_primary',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
