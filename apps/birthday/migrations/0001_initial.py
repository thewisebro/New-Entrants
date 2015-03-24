# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BirthdayMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=500)),
                ('reply', models.CharField(max_length=500, blank=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('receiver', models.ForeignKey(related_name=b'got_birthday_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name=b'send_birthday_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
