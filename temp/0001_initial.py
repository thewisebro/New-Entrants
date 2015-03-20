# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyMails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('by_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BuySellCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('main_category', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(unique=True, max_length=100)),
                ('watch_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RequestedItems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('trashed', models.BooleanField(default=False)),
                ('datetime_trashed', models.DateTimeField(null=True, blank=True)),
                ('item_name', models.CharField(max_length=100)),
                ('condition', models.CharField(max_length=100, choices=[(b'Excellent', b'Excellent'), (b'Good', b'Good'), (b'Fine', b'Fine'), (b'Old', b'Old')])),
                ('price_upper', models.IntegerField(max_length=10)),
                ('price_lower', models.IntegerField(default=0, max_length=10, blank=True)),
                ('post_date', core.models.fields.DateField()),
                ('days_till_expiry', models.IntegerField(max_length=2, choices=[(10, b'10'), (15, b'15'), (20, b'20'), (25, b'25'), (30, b'30'), (45, b'45'), (60, b'60')])),
                ('expiry_date', core.models.fields.DateField()),
                ('contact', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=75)),
                ('show_contact', models.BooleanField(default=True)),
                ('category', models.ForeignKey(to='buyandsell.BuySellCategory')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RequestMails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('by_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(to='buyandsell.RequestedItems')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SaleItems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('trashed', models.BooleanField(default=False)),
                ('datetime_trashed', models.DateTimeField(null=True, blank=True)),
                ('item_name', models.CharField(max_length=100)),
                ('cost', models.IntegerField(max_length=10)),
                ('status', models.CharField(max_length=100, choices=[(b'Excellent', b'Excellent'), (b'Good', b'Good'), (b'Fine', b'Fine'), (b'Old', b'Old')])),
                ('detail', models.TextField()),
                ('contact', models.CharField(max_length=10)),
                ('post_date', core.models.fields.DateField()),
                ('days_till_expiry', models.IntegerField(max_length=2, choices=[(10, b'10'), (15, b'15'), (20, b'20'), (25, b'25'), (30, b'30'), (45, b'45'), (60, b'60')])),
                ('expiry_date', core.models.fields.DateField()),
                ('email', models.EmailField(max_length=75)),
                ('item_image', models.ImageField(default=b'../static/images/buysell/default.png', upload_to=b'buyandsell/images', blank=True)),
                ('show_contact', models.BooleanField(default=True)),
                ('category', models.ForeignKey(to='buyandsell.BuySellCategory')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShowContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('contact_shown', models.BooleanField(default=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SuccessfulTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('is_requested', models.BooleanField(default=False)),
                ('trasaction_date', core.models.fields.DateField()),
                ('feedback', models.TextField()),
                ('buyer', models.ForeignKey(related_name=b'suc_trans_buyer', to=settings.AUTH_USER_MODEL)),
                ('request_item', models.OneToOneField(blank=True, to='buyandsell.RequestedItems')),
                ('sell_item', models.OneToOneField(blank=True, to='buyandsell.SaleItems')),
                ('seller', models.ForeignKey(related_name=b'suc_trans_seller', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='buymails',
            name='item',
            field=models.ForeignKey(to='buyandsell.SaleItems'),
            preserve_default=True,
        ),
    ]
