# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LectutDesignChoice',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('faculty_id', models.CharField(max_length=45)),
                ('choice', models.IntegerField()),
            ],
            options={
                'db_table': 'lectut_design_choice',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LectutExamPapers',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('faculty_id', models.CharField(max_length=45)),
                ('course_id', models.CharField(max_length=24)),
                ('file', models.CharField(max_length=450)),
                ('topic', models.CharField(max_length=450)),
                ('permission', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
                ('year', models.CharField(max_length=45, blank=True)),
            ],
            options={
                'db_table': 'lectut_exam_papers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LectutLectures',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('faculty_id', models.CharField(max_length=45)),
                ('course_id', models.CharField(max_length=24)),
                ('file', models.CharField(max_length=450)),
                ('topic', models.CharField(max_length=450)),
                ('permission', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
            ],
            options={
                'db_table': 'lectut_lectures',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LectutSolutions',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('faculty_id', models.CharField(max_length=45)),
                ('course_id', models.CharField(max_length=24)),
                ('file', models.CharField(max_length=450)),
                ('topic', models.CharField(max_length=450)),
                ('permission', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
                ('link_type', models.CharField(max_length=3, blank=True)),
                ('link_id', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'lectut_solutions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LectutTutorials',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('faculty_id', models.CharField(max_length=45)),
                ('course_id', models.CharField(max_length=24)),
                ('file', models.CharField(max_length=450)),
                ('topic', models.CharField(max_length=450)),
                ('permission', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
            ],
            options={
                'db_table': 'lectut_tutorials',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VleAdmin',
            fields=[
                ('slno', models.IntegerField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=30, blank=True)),
                ('perm', models.CharField(max_length=30, blank=True)),
            ],
            options={
                'db_table': 'vle_admin',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VleAnsagree',
            fields=[
                ('aid', models.IntegerField(null=True, blank=True)),
                ('user_id', models.CharField(max_length=30, blank=True)),
                ('slno', models.IntegerField(serialize=False, primary_key=True)),
                ('qid', models.IntegerField(null=True, blank=True)),
                ('agree', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'vle_ansagree',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VleAnswers',
            fields=[
                ('ans_id', models.IntegerField(serialize=False, primary_key=True)),
                ('qid', models.IntegerField(null=True, blank=True)),
                ('ans', models.TextField(blank=True)),
                ('post_time', models.DateTimeField()),
                ('user_id', models.CharField(max_length=30, blank=True)),
                ('flagger', models.CharField(max_length=30, blank=True)),
                ('flag', models.IntegerField(null=True, blank=True)),
                ('agrees', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'vle_answers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VleCategory',
            fields=[
                ('category', models.IntegerField(serialize=False, primary_key=True)),
                ('category_name', models.CharField(max_length=150, blank=True)),
            ],
            options={
                'db_table': 'vle_category',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VleFiles',
            fields=[
                ('fid', models.IntegerField(serialize=False, primary_key=True)),
                ('qid', models.IntegerField(null=True, blank=True)),
                ('aid', models.IntegerField(null=True, blank=True)),
                ('filename', models.CharField(max_length=150, blank=True)),
                ('upload_time', models.DateTimeField()),
                ('mimetype', models.CharField(max_length=420, blank=True)),
            ],
            options={
                'db_table': 'vle_files',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VleFollowuser',
            fields=[
                ('slno', models.IntegerField(serialize=False, primary_key=True)),
                ('followed', models.CharField(max_length=30, blank=True)),
                ('follower', models.CharField(max_length=30, blank=True)),
            ],
            options={
                'db_table': 'vle_followuser',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VleQfollowed',
            fields=[
                ('qid', models.IntegerField(null=True, blank=True)),
                ('user_id', models.CharField(max_length=30, blank=True)),
                ('sl', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'vle_qfollowed',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VleQuesliked',
            fields=[
                ('sl', models.IntegerField(serialize=False, primary_key=True)),
                ('qid', models.IntegerField(null=True, blank=True)),
                ('user_id', models.CharField(max_length=30, blank=True)),
            ],
            options={
                'db_table': 'vle_quesliked',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VleQuestions',
            fields=[
                ('qid', models.IntegerField(serialize=False, primary_key=True)),
                ('user_id', models.CharField(max_length=30, blank=True)),
                ('text', models.TextField(blank=True)),
                ('post_time', models.DateTimeField()),
                ('last_activity', models.DateTimeField()),
                ('category', models.CharField(max_length=30, blank=True)),
                ('status', models.IntegerField(null=True, blank=True)),
                ('tags', models.CharField(max_length=300, blank=True)),
                ('files', models.CharField(max_length=3000, blank=True)),
                ('open', models.IntegerField(null=True, blank=True)),
                ('flag', models.IntegerField(null=True, blank=True)),
                ('flagger', models.CharField(max_length=30, blank=True)),
            ],
            options={
                'db_table': 'vle_questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VleUsers',
            fields=[
                ('sl', models.IntegerField(serialize=False, primary_key=True)),
                ('user_id', models.CharField(max_length=24, blank=True)),
                ('rating', models.IntegerField(null=True, blank=True)),
                ('name', models.CharField(max_length=240, blank=True)),
            ],
            options={
                'db_table': 'vle_users',
            },
            bases=(models.Model,),
        ),
    ]
