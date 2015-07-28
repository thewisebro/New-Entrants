# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields
import crop_image.base
import core.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0006_auto_20150507_1746'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(unique=True, max_length=100)),
                ('short_description', models.TextField()),
                ('content', redactor.fields.RedactorField()),
                ('date', core.models.fields.DateTimeField()),
                ('state', models.CharField(default=b'Unpublished', max_length=12, choices=[(b'Published', b'Published'), (b'Unpublished', b'Unpublished')])),
                ('slug', models.SlugField(max_length=150)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('message', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MemberLinks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('website', models.CharField(max_length=100, choices=[(b'facebook', b'Facebook'), (b'quora', b'Quora'), (b'twitter', b'Twitter'), (b'googleplus', b'Google Plus'), (b'github', b'Github'), (b'linkedin', b'LinkedIn')])),
                ('link', models.URLField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RecentWorks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(unique=True, max_length=100)),
                ('image', models.ImageField(upload_to=b'img_website/works/')),
                ('short_description', models.TextField()),
                ('content', redactor.fields.RedactorField()),
                ('date', core.models.fields.DateTimeField()),
                ('state', models.CharField(default=b'Unpublished', max_length=12, choices=[(b'Published', b'Published'), (b'Unpublished', b'Unpublished')])),
                ('category', models.CharField(default=b'Intranet', max_length=12, choices=[(b'Intranet', b'Intranet'), (b'Internet', b'Internet')])),
                ('slug', models.SlugField(max_length=150)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatusPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('content', redactor.fields.RedactorField()),
                ('date', core.models.fields.DateTimeField()),
                ('state', models.CharField(default=b'Unpublished', max_length=12, choices=[(b'Published', b'Published'), (b'Unpublished', b'Unpublished')])),
                ('app', models.CharField(max_length=40)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('member_pic', crop_image.base.CropImageModelField(upload_to=b'img_website/team/', blank=True)),
                ('member_post', models.CharField(default=b'Developer', max_length=20, choices=[(b'Developer', b'Developer'), (b'Designer', b'Designer')])),
                ('member_status', models.CharField(default=b'Current', max_length=20, choices=[(b'Current', b'Current'), (b'Alumni', b'Alumni')])),
                ('member_about', models.CharField(max_length=200)),
                ('member_name', models.ForeignKey(to='nucleus.Student', unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='memberlinks',
            name='teammember',
            field=models.ForeignKey(to='img_website.TeamMember'),
            preserve_default=True,
        ),
    ]
