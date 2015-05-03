# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jukebox.models
from django.conf import settings
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('album', models.CharField(max_length=100)),
                ('year', models.IntegerField(default=2015, max_length=4)),
                ('album_art', models.ImageField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/uploads', location=b'/home/songsmedia/'), upload_to=b'albumart/')),
                ('language', models.CharField(max_length=10, choices=[(b'eng', b'English'), (b'hindi', b'Hindi'), (b'tamil', b'Tamil'), (b'telugu', b'Telugu'), (b'punjabi', b'Punjabi'), (b'mal', b'Malyali')])),
                ('latest', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('artist', models.CharField(max_length=100)),
                ('cover_pic', models.ImageField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/uploads', location=b'/home/songsmedia/'), upload_to=b'artist/')),
                ('language', models.CharField(max_length=10, choices=[(b'eng', b'English'), (b'hindi', b'Hindi'), (b'tamil', b'Tamil'), (b'telugu', b'Telugu'), (b'punjabi', b'Punjabi'), (b'mal', b'Malyali')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('genre', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Jukebox_Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('songs_listen', models.TextField()),
                ('person', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('songs', models.TextField(null=True, blank=True)),
                ('private', models.BooleanField(default=True)),
                ('public_count', models.PositiveIntegerField(default=0)),
                ('liked_by', models.ManyToManyField(related_name=b'jukebox_playlist_likes', to=settings.AUTH_USER_MODEL)),
                ('person', models.ForeignKey(to='jukebox.Jukebox_Person')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('id_no', models.IntegerField(default=0, max_length=100)),
                ('song', models.CharField(max_length=100)),
                ('file_name', models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/uploads', location=b'/home/songsmedia/songs/english/'), max_length=1000, upload_to=jukebox.models.content_file_name)),
                ('language', models.CharField(max_length=10, choices=[(b'eng', b'English'), (b'hindi', b'Hindi'), (b'tamil', b'Tamil'), (b'telugu', b'Telugu'), (b'punjabi', b'Punjabi'), (b'mal', b'Malyali')])),
                ('count', models.PositiveIntegerField(default=0)),
                ('score', models.PositiveIntegerField(default=0)),
                ('album', models.ForeignKey(to='jukebox.Album', null=True)),
                ('artists', models.ManyToManyField(to='jukebox.Artist')),
                ('genres', models.ManyToManyField(to='jukebox.Genre')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='album',
            name='artists',
            field=models.ManyToManyField(to='jukebox.Artist', null=True, blank=True),
            preserve_default=True,
        ),
    ]
