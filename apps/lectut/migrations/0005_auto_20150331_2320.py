# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lectut', '0004_auto_20150327_2300'),
    ]

    operations = [
        migrations.CreateModel(
            name='post_comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=100)),
                ('post', models.ForeignKey(to='lectut.Post')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='activity',
            name='content_type',
        ),
        migrations.DeleteModel(
            name='Activity',
        ),
        migrations.RemoveField(
            model_name='uploadfile',
            name='batch',
        ),
        migrations.RemoveField(
            model_name='uploadfile',
            name='upload_user',
        ),
        migrations.DeleteModel(
            name='UploadFile',
        ),
        migrations.RenameField(
            model_name='downloadlog',
            old_name='uploadfile',
            new_name='uploadedfile',
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='download_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reminders',
            name='event_date',
            field=core.models.fields.DateTimeField(default=datetime.datetime(2015, 4, 7, 23, 19, 52, 46310)),
        ),
    ]
