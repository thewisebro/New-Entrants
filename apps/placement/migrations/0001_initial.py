# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import core.models.fields
import django.core.validators


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
                ('name', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('status', models.CharField(max_length=3, choices=[(b'OPN', b'Open'), (b'CLS', b'Closed'), (b'DEC', b'Declared'), (b'FIN', b'Finalized')])),
                ('place_of_posting', models.CharField(max_length=100, blank=True)),
                ('category', models.CharField(max_length=3, choices=[(b'A', b'A'), (b'B', b'B'), (b'C', b'C'), (b'U', b'University')])),
                ('latest_date_of_joining', core.models.fields.DateField(null=True, blank=True)),
                ('package_ug', models.CharField(max_length=20, null=True, verbose_name=b'CTC(UG)', blank=True)),
                ('package_pg', models.CharField(max_length=20, null=True, verbose_name=b'CTC(PG)', blank=True)),
                ('package_phd', models.CharField(max_length=20, null=True, verbose_name=b'CTC(PhD)', blank=True)),
                ('ctc_remark', models.CharField(max_length=100, null=True, verbose_name=b'CTC Remark', blank=True)),
                ('cgpa_requirement', models.FloatField(blank=True, null=True, verbose_name=b'CGPA Requirement', choices=[(5.0, b'5.0'), (5.25, b'5.25'), (5.5, b'5.5'), (5.75, b'5.75'), (6.0, b'6.0'), (6.25, b'6.25'), (6.5, b'6.5'), (6.75, b'6.75'), (7.0, b'7.0'), (7.25, b'7.25'), (7.5, b'7.5'), (7.75, b'7.75'), (8.0, b'8.0'), (8.25, b'8.25'), (8.5, b'8.5'), (8.75, b'8.75'), (9.0, b'9.0')])),
                ('company_description', models.TextField(blank=True)),
                ('pre_placement_talk', core.models.fields.DateField(null=True, blank=True)),
                ('shortlist_from_resumes', models.BooleanField(default=False)),
                ('group_discussion', models.BooleanField(default=False)),
                ('online_test', models.BooleanField(default=False)),
                ('written_test', models.BooleanField(default=False)),
                ('paper_based_test', models.BooleanField(default=False)),
                ('interview_1', models.BooleanField(default=False, verbose_name=b'Interview(In Person)')),
                ('interview_2', models.BooleanField(default=False, verbose_name=b'Interview(Video Conferencing)')),
                ('interview_3', models.BooleanField(default=False, verbose_name=b'Interview(Skype)')),
                ('last_date_of_applying', core.models.fields.DateTimeField(null=True, blank=True)),
                ('name_of_post', models.CharField(max_length=100, blank=True)),
                ('description_of_post', models.TextField(blank=True)),
                ('other_requirements', models.CharField(max_length=100, blank=True)),
                ('total_vacancies_for_iitr', models.IntegerField(null=True, verbose_name=b'Total vacancies for IITR', blank=True)),
                ('website', models.CharField(max_length=100, blank=True)),
                ('brochure', core.models.fields.AutoDeleteFileField(null=True, upload_to=b'placement/brochures/', blank=True)),
                ('sector', models.CharField(max_length=3, choices=[(b'FIN', b'Finance'), (b'PSU', b'PSU/Government'), (b'CON', b'Consultancy'), (b'FMC', b'FMCG'), (b'PHA', b'Pharmaceuticals'), (b'RnD', b'R&D'), (b'IT', b'IT'), (b'ACA', b'Academics'), (b'OIL', b'Oil & Gas'), (b'CIN', b'Construction / Infrastructure'), (b'COR', b'Core Engineering')])),
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
                ('shortlisted', models.BooleanField(default=False)),
                ('time_of_application', core.models.fields.DateTimeField(default=datetime.datetime(2015, 1, 17, 18, 26, 9, 93838))),
                ('company', models.ForeignKey(to='placement.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('company_name', models.CharField(max_length=250)),
                ('cluster', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4)])),
                ('status', models.CharField(blank=True, max_length=40, null=True, choices=[(b'JAF Sent', b'JAF Sent'), (b'JAF Received', b'JAF Received'), (b'STF Sent', b'STF Sent'), (b'Not Called', b'Not Called'), (b'JAF + STF sent', b'JAF + STF sent'), (b'JAF+ STF recieved', b'JAF+ STF recieved'), (b'Not Picking Up', b'Not Picking Up'), (b'Incorrect contact info', b'Incorrect contact info'), (b'Call Later', b'call later'), (b'Denied', b'Denied'), (b'Process Confirmed', b'Process Confirmed'), (b'Other', b'Other')])),
                ('last_contact', models.CharField(max_length=100, null=True, blank=True)),
                ('person_in_contact', models.CharField(max_length=100, null=True, blank=True)),
                ('comments', models.TextField(null=True, blank=True)),
                ('when_to_contact', core.models.fields.DateField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyCoordi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyPlacementPriority',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('priority', models.IntegerField(null=True, blank=True)),
                ('date_created', core.models.fields.DateTimeField(auto_now_add=True)),
                ('date_updated', core.models.fields.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(to='placement.Company')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanySlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('visibility', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=True)),
                ('start_date', core.models.fields.DateTimeField(null=True, blank=True)),
                ('end_date', core.models.fields.DateTimeField(null=True, blank=True)),
                ('company', models.ManyToManyField(to='placement.Company')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('contact_person', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=100, null=True, blank=True)),
                ('phone_no', models.CharField(max_length=250, null=True, blank=True)),
                ('email', models.CharField(max_length=250, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CPTMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('contact_no', models.CharField(max_length=15)),
                ('year', models.IntegerField()),
                ('email', models.EmailField(max_length=75)),
                ('currently_a_member', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EducationalDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('year', models.IntegerField()),
                ('sgpa', models.FloatField(default=0.0, verbose_name=b'SGPA')),
                ('cgpa', models.FloatField(default=0.0, verbose_name=b'CGPA')),
                ('course', models.CharField(max_length=4, choices=[(b'UG0', b'UG Overall'), (b'DPLM', b'Diploma'), (b'PG0', b'PG Overall'), (b'10TH', b'Tenth'), (b'12TH', b'Twelfth'), (b'UG10', b'UG(I Year I Semester)'), (b'UG11', b'UG(I Year II Semester)'), (b'UG20', b'UG(II Year I Semester)'), (b'UG21', b'UG(II Year II Semester)'), (b'UG30', b'UG(III Year I Semester)'), (b'UG31', b'UG(III Year II Semester)'), (b'UG40', b'UG(IV Year I Semester)'), (b'UG41', b'UG(IV Year II Semester)'), (b'UG50', b'UG(V Year I Semester)'), (b'UG51', b'UG(V Year II Semester)'), (b'ST1', b'Summer Term(I Year)'), (b'ST2', b'Summer Term(II Year)'), (b'ST3', b'Summer Term(III Year)'), (b'ST4', b'Summer Term(IV Year)'), (b'PG10', b'PG(I Year I Semester)'), (b'PG11', b'PG(I Year II Semester)'), (b'PG20', b'PG(II Year I Semester)'), (b'PG21', b'PG(II Year II Semester)'), (b'PG30', b'PG(III Year I Semester)'), (b'PG31', b'PG(III Year II Semester)'), (b'PHD10', b'PHD(I Year I Semester)'), (b'PHD11', b'PHD(I Year II Semester)'), (b'PHD20', b'PHD(II Year I Semester)'), (b'PHD21', b'PHD(II Year II Semester)'), (b'PHD30', b'PHD(III Year I Semester)'), (b'PHD31', b'PHD(III Year II Semester)'), (b'PHD40', b'PHD(IV Year I Semester)'), (b'PHD41', b'PHD(IV Year II Semester)'), (b'PHD50', b'PHD(V Year I Semester)'), (b'PHD51', b'PHD(V Year II Semester)'), (b'PHD60', b'PHD(VI Year I Semester)'), (b'PHD61', b'PHD(VI Year II Semester)'), (b'PHD70', b'PHD(VII Year I Semester)'), (b'PHD71', b'PHD(VII Year II Semester)'), (b'PHD80', b'PHD(VIII Year I Semester)'), (b'PHD81', b'PHD(VIII Year II Semester)'), (b'PHD90', b'PHD(IX Year I Semester)'), (b'PHD91', b'PHD(IX Year II Semester)'), (b'PHD0', b'PHD Overall'), (b'UG00', b'UG(New Entrants)')])),
                ('institution', models.CharField(max_length=100)),
                ('discipline', models.CharField(max_length=10)),
                ('discipline_provided', models.CharField(max_length=100, blank=True)),
                ('student', models.ForeignKey(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExtraCurriculars',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('name_of_activity', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=100, blank=True)),
                ('achievement', models.TextField()),
                ('priority', models.IntegerField(default=1, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visible', models.BooleanField(default=True)),
                ('student', models.ForeignKey(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Facebook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('internship', models.TextField(validators=[django.core.validators.MaxLengthValidator(70)])),
                ('projects', models.TextField(validators=[django.core.validators.MaxLengthValidator(70)])),
                ('extra_curriculars', models.TextField(validators=[django.core.validators.MaxLengthValidator(70)])),
                ('b_tech_degree', models.CharField(max_length=100, blank=True)),
                ('student', models.OneToOneField(to='nucleus.Student')),
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
                ('feedback', models.TextField()),
                ('date', core.models.fields.DateField(auto_now_add=True)),
                ('company', models.ForeignKey(to='placement.Company')),
                ('student', models.ForeignKey(to='nucleus.Student')),
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
                ('post', models.ForeignKey(to='placement.ForumPost')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InternshipInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('brief_description', models.TextField(blank=True)),
                ('industry', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('period', models.CharField(max_length=100)),
                ('priority', models.IntegerField(default=1, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visible', models.BooleanField(default=True)),
                ('student', models.ForeignKey(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JobExperiences',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('organisation', models.CharField(max_length=100)),
                ('post', models.CharField(max_length=100)),
                ('date_of_joining', core.models.fields.DateField()),
                ('date_of_leaving', core.models.fields.DateField()),
                ('brief_description', models.TextField()),
                ('priority', models.IntegerField(default=1, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visible', models.BooleanField(default=True)),
                ('student', models.ForeignKey(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LanguagesKnown',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('language', models.CharField(max_length=3, choices=[(b'AB', b'Arabic'), (b'AS', b'Assamese'), (b'BN', b'Bangla'), (b'EN', b'English'), (b'FR', b'French'), (b'GM', b'German'), (b'GJ', b'Gujarati'), (b'HB', b'Hebrew'), (b'HN', b'Hindi'), (b'JA', b'Japanese'), (b'KD', b'Kannada'), (b'MM', b'Malyalam'), (b'MR', b'Marathi'), (b'NP', b'Nepali'), (b'OR', b'Oriya'), (b'PN', b'Punjabi'), (b'RU', b'Russian'), (b'SN', b'Sanskrit'), (b'SP', b'Spanish'), (b'SW', b'Swahili'), (b'TM', b'Tamil'), (b'TG', b'Telugu'), (b'UD', b'Urdu')])),
                ('proficiency', models.CharField(max_length=3, choices=[(b'SRW', b'Speak, Read and Write'), (b'SO', b'Speak Only'), (b'RW', b'Read and Write'), (b'SR', b'Speak and Read')])),
                ('student', models.ForeignKey(to='nucleus.Student')),
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
                ('notice', core.models.fields.AutoDeleteFileField(help_text=b"<span style='margin-left:70px; font-size:0.8em'>Allowed extensions : 'txt', 'doc', 'pdf', 'xml', 'xls', 'xlsx'</span>", upload_to=b'placement/notices/')),
                ('date_of_upload', core.models.fields.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlacementInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('registration_no', models.CharField(max_length=50, blank=True)),
                ('area_of_interest', models.CharField(max_length=100, blank=True)),
                ('computer_languages', models.CharField(max_length=100, blank=True)),
                ('software_packages', models.TextField(blank=True)),
                ('achievements', models.TextField(blank=True)),
                ('course_taken', models.TextField(verbose_name=b'Additional Courses Taken', blank=True)),
                ('reference_1', models.CharField(max_length=100, blank=True)),
                ('designation_1', models.CharField(max_length=100, blank=True)),
                ('institute_1', models.CharField(max_length=100, blank=True)),
                ('email_1', models.EmailField(max_length=75, blank=True)),
                ('phone_1', models.CharField(max_length=25, blank=True)),
                ('reference_2', models.CharField(max_length=100, blank=True)),
                ('designation_2', models.CharField(max_length=100, blank=True)),
                ('institute_2', models.CharField(max_length=100, blank=True)),
                ('email_2', models.EmailField(max_length=75, blank=True)),
                ('phone_2', models.CharField(max_length=25, blank=True)),
                ('student', models.OneToOneField(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlacementMgr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('company_name', models.ForeignKey(to='placement.CompanyContact')),
                ('coordi', models.ForeignKey(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlacementPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('placed_company_category', models.CharField(blank=True, max_length=3, null=True, choices=[(b'A', b'A'), (b'B', b'B'), (b'C', b'C'), (b'U', b'University')])),
                ('no_of_companies_placed', models.IntegerField(default=0)),
                ('status', models.CharField(default=b'CLS', max_length=3, choices=[(b'CLS', b'Closed'), (b'OPN', b'Opened'), (b'LCK', b'Locked'), (b'VRF', b'Verified')])),
                ('photo', core.models.fields.AutoDeleteImageField(help_text=b"<span style='margin-left:-70px;font-size:0.9em;'>Recommended size: <b>35mm width x 45mm height</b></span>", null=True, upload_to=b'placement/photos/', blank=True)),
                ('is_debarred', models.BooleanField(default=False)),
                ('student', models.OneToOneField(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('brief_description', models.TextField(blank=True)),
                ('industry', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('period', models.CharField(max_length=100)),
                ('priority', models.IntegerField(default=1, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visible', models.BooleanField(default=True)),
                ('student', models.ForeignKey(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResearchPublications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('author', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('publisher', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('priority', models.IntegerField(default=1, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visible', models.BooleanField(default=True)),
                ('student', models.ForeignKey(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(to='placement.Company')),
                ('student', models.ForeignKey(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SecondRound',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('year', models.IntegerField()),
                ('branch', models.ForeignKey(to='nucleus.Branch')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkshopPriority',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('day1_priority', models.IntegerField(default=0)),
                ('day2_priority', models.IntegerField(default=0)),
                ('day3_priority', models.IntegerField(default=0)),
                ('day4_priority', models.IntegerField(default=0)),
                ('day5_priority', models.IntegerField(default=0)),
                ('interview_application', models.BooleanField(default=False)),
                ('student', models.ForeignKey(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='companyplacementpriority',
            name='slots',
            field=models.ForeignKey(to='placement.CompanySlot'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companyplacementpriority',
            name='student',
            field=models.ForeignKey(to='nucleus.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companycontact',
            name='contactperson',
            field=models.ForeignKey(blank=True, to='placement.ContactPerson', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companyapplicationmap',
            name='plac_person',
            field=models.ForeignKey(to='placement.PlacementPerson'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='companyapplicationmap',
            unique_together=set([('plac_person', 'company')]),
        ),
        migrations.AddField(
            model_name='company',
            name='contact_person',
            field=models.ForeignKey(blank=True, to='placement.CPTMember', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='open_for_disciplines',
            field=models.ManyToManyField(to='nucleus.Branch'),
            preserve_default=True,
        ),
    ]
