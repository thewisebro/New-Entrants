# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import jukebox.models


class Migration(migrations.Migration):

    dependencies = [
        ('jukebox', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album_art',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/uploads', location=b'/home/apps/nas/songsmedia/'), upload_to=b'albumart/'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='cover_pic',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/uploads', location=b'/home/apps/nas/songsmedia/'), upload_to=b'artist/'),
        ),
        migrations.AlterField(
            model_name='song',
            name='file_name',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/uploads', location=b'/home/apps/nas/songsmedia/songs/english/'), max_length=1000, upload_to=jukebox.models.content_file_name),
        ),
    ]
