# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('soft_name', models.CharField(max_length=100, verbose_name=b'Software Name')),
                ('category', models.CharField(max_length=80, choices=[(b'internet', b'Internet'), (b'antimalware', b'Anti-Malware'), (b'multimedia', b'Multimedia'), (b'p2p', b'Filesharing'), (b'security', b'Security'), (b'dvd', b'DVD Tools'), (b'messaging', b'Messaging'), (b'system_tuning', b'System Tuning'), (b'desktop', b'Desktop'), (b'file_transfer', b'File Transfer'), (b'archiving', b'Archiving'), (b'photos_images', b'Photos & Images'), (b'office', b'Office & News'), (b'networking', b'Networking'), (b'drivers', b'Drivers'), (b'developer', b'Developer Tools')])),
                ('image', models.ImageField(upload_to=b'softwares/images')),
                ('url', models.URLField(verbose_name=b'URL')),
                ('version', models.CharField(max_length=100, null=True, verbose_name=b'Version', blank=True)),
                ('description', models.TextField(max_length=1000, null=True, blank=True)),
                ('date_added', models.DateTimeField(default=datetime.datetime(2015, 3, 20, 17, 8, 31, 253712), verbose_name=b'Date Added')),
                ('download_count', models.IntegerField(default=0, verbose_name=b'Downloads')),
                ('added_by', models.CharField(max_length=20, verbose_name=b'Uploaded By')),
                ('soft_file', models.FileField(upload_to=b'softwares/binaries', verbose_name=b'File')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
