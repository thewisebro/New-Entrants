# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('name_of_company', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=3, choices=[(b'OPN', b'Open'), (b'CLS', b'Closed'), (b'DEC', b'Declared'), (b'FIN', b'Finalized')])),
                ('year', models.IntegerField()),
                ('address', models.CharField(max_length=100, blank=True)),
                ('latest_date_of_joining', models.CharField(max_length=100, blank=True)),
                ('stipend', models.CharField(max_length=100, blank=True)),
                ('stipend_remark', models.CharField(max_length=100, blank=True)),
                ('cgpa_requirements', models.CharField(max_length=100, verbose_name=b'CGPA Requirements', blank=True)),
                ('description', models.TextField(blank=True)),
                ('designation_of_contact_person', models.CharField(max_length=100, blank=True)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('fax', models.CharField(max_length=100, blank=True)),
                ('last_date_of_applying', models.CharField(max_length=100, blank=True)),
                ('name_of_contact_person', models.CharField(max_length=100, blank=True)),
                ('nature_of_duties', models.CharField(max_length=100, blank=True)),
                ('name_of_post', models.CharField(max_length=100, blank=True)),
                ('no_of_employees', models.IntegerField(null=True, blank=True)),
                ('other_requirements', models.CharField(max_length=100, blank=True)),
                ('telephone', models.CharField(max_length=100, blank=True)),
                ('pre_internship_talk', models.BooleanField(default=False)),
                ('shortlist_from_resumes', models.BooleanField(default=False)),
                ('group_discussion', models.BooleanField(default=False)),
                ('online_test', models.BooleanField(default=False)),
                ('written_test', models.BooleanField(default=False)),
                ('paper_based_test', models.BooleanField(default=False)),
                ('interview_1', models.BooleanField(default=False, verbose_name=b'Interview(In Person)')),
                ('interview_2', models.BooleanField(default=False, verbose_name=b'Interview(Video Conferencing)')),
                ('interview_3', models.BooleanField(default=False, verbose_name=b'Interview(Skype)')),
                ('probable_date_of_arrival', models.CharField(max_length=100, blank=True)),
                ('total_vacancies', models.IntegerField(null=True, blank=True)),
                ('training_period', models.CharField(max_length=100, blank=True)),
                ('turnover', models.CharField(max_length=100, blank=True)),
                ('website', models.CharField(max_length=100, blank=True)),
                ('brochure', core.models.fields.AutoDeleteFileField(null=True, upload_to=b'internship/brochures/', blank=True)),
                ('sector', models.CharField(max_length=2, choices=[(b'NA', b'Not Applicable'), (b'FI', b'Finance'), (b'PG', b'PSU/Government'), (b'CO', b'Consultancy'), (b'FM', b'FMCG'), (b'PH', b'Pharmaceuticals'), (b'RD', b'R&D'), (b'IT', b'IT'), (b'AC', b'Academics'), (b'OG', b'Oil & Gas'), (b'CI', b'Construction/Infrastructure'), (b'CE', b'Core Engineering')])),
                ('open_for_disciplines', models.ManyToManyField(related_name=b'internship_company_related', to='nucleus.Branch')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyApplicationMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=3, choices=[(b'APP', b'Applied'), (b'FIN', b'Finalized'), (b'SEL', b'Selected')])),
                ('company', models.ForeignKey(to='internship.Company')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyPriority',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('priority', models.IntegerField(default=0)),
                ('company', models.ForeignKey(to='internship.Company')),
                ('student', models.ForeignKey(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('enrollment_no', models.CharField(max_length=10)),
                ('person_name', models.CharField(max_length=100)),
                ('discipline_name', models.CharField(max_length=100)),
                ('department_name', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=100)),
                ('feedback', models.TextField()),
                ('date', core.models.fields.DateField()),
                ('year', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('enrollment_no', models.CharField(max_length=10)),
                ('person_name', models.CharField(max_length=100)),
                ('discipline_name', models.CharField(max_length=100)),
                ('department_name', models.CharField(max_length=100)),
                ('title', models.TextField()),
                ('content', models.TextField()),
                ('date', core.models.fields.DateTimeField(auto_now_add=True)),
                ('forum_type', models.CharField(max_length=3, choices=[(b'T', b'Technical'), (b'P', b'Placement')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumReply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('enrollment_no', models.CharField(max_length=10)),
                ('person_name', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('date', core.models.fields.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(to='internship.ForumPost')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InternshipPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=3, choices=[(b'CLS', b'Closed'), (b'OPN', b'Opened')])),
                ('is_placed', models.BooleanField(default=False)),
                ('student', models.OneToOneField(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('notice', core.models.fields.AutoDeleteFileField(help_text=b"<span style='margin-left:70px; font-size:0.8em'>Allowed extensions : 'txt', 'doc', 'pdf', 'xml', 'xls', 'xlsx'</span>", upload_to=b'internship/notices/')),
                ('date_of_upload', core.models.fields.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('enrollment_no', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('person_name', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=100)),
                ('discipline_name', models.CharField(max_length=100)),
                ('department_name', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('company_id', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResultsNew',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(to='internship.Company')),
                ('student', models.ForeignKey(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='companyapplicationmap',
            name='student',
            field=models.ForeignKey(to='internship.InternshipPerson'),
            preserve_default=True,
        ),
    ]
