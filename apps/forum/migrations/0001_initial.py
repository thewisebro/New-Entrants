# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields
import taggit_autocomplete.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('nucleus', '__first__'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('activity_type', models.CharField(max_length=10, choices=[(b'ASK_QUES', b'Asked Question'), (b'POST_ANS', b'Posted Answer'), (b'FOL_TOPIC', b'Followed Topic'), (b'FOL_QUES', b'Followed question'), (b'UP_ANS', b'Upvoted Answer')])),
                ('object_id', models.IntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('datetime_modified', core.models.fields.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('student', models.OneToOneField(primary_key=True, serialize=False, to='nucleus.Student')),
                ('answers_down', models.ManyToManyField(related_name=b'downvoted_by', null=True, to='forum.Answer', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProfileAnswerUpvoted',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('answer', models.ForeignKey(to='forum.Answer')),
                ('profile', models.ForeignKey(to='forum.Profile')),
            ],
            options={
                'db_table': 'forum_profile_answers_up',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProfileQuestionFollowed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(to='forum.Profile')),
            ],
            options={
                'db_table': 'forum_profile_questions_followed',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', core.models.fields.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('title', models.CharField(max_length=100)),
                ('profile', models.ForeignKey(related_name=b'added', to='forum.Profile')),
                ('tags', taggit_autocomplete.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
                ('user_views', models.ManyToManyField(related_name=b'viewed', to='forum.Profile')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='profilequestionfollowed',
            name='question',
            field=models.ForeignKey(to='forum.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='answers_up',
            field=models.ManyToManyField(related_name=b'upvoted_by', null=True, through='forum.ProfileAnswerUpvoted', to='forum.Answer', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='questions_followed',
            field=models.ManyToManyField(related_name=b'following_profiles', null=True, through='forum.ProfileQuestionFollowed', to='forum.Question', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='tags_followed',
            field=taggit_autocomplete.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='profile',
            field=models.ForeignKey(to='forum.Profile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name=b'answers', to='forum.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='profile',
            field=models.ForeignKey(to='forum.Profile'),
            preserve_default=True,
        ),
    ]
