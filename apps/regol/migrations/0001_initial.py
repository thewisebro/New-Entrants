# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0006_auto_20150417_0353'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedFaculty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('branch', models.ForeignKey(to='nucleus.Branch')),
                ('faculty', models.ForeignKey(to='nucleus.Faculty')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseDetails',
            fields=[
                ('course_code', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('course_name', models.CharField(max_length=100)),
                ('credits', models.IntegerField()),
                ('group_code', models.CharField(default=b'-1', max_length=100)),
                ('seats', models.IntegerField(null=True, blank=True)),
                ('pre_requisite', models.ForeignKey(blank=True, to='regol.CourseDetails', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseStructureMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_code', models.CharField(max_length=10)),
                ('semester', models.CharField(max_length=100, choices=[(b'UG0', b'UG Overall'), (b'DPLM', b'Diploma'), (b'PG0', b'PG Overall'), (b'10TH', b'Tenth'), (b'12TH', b'Twelfth'), (b'UG10', b'UG(I Year I Semester)'), (b'UG11', b'UG(I Year II Semester)'), (b'UG20', b'UG(II Year I Semester)'), (b'UG21', b'UG(II Year II Semester)'), (b'UG30', b'UG(III Year I Semester)'), (b'UG31', b'UG(III Year II Semester)'), (b'UG40', b'UG(IV Year I Semester)'), (b'UG41', b'UG(IV Year II Semester)'), (b'UG50', b'UG(V Year I Semester)'), (b'UG51', b'UG(V Year II Semester)'), (b'ST1', b'Summer Term(I Year)'), (b'ST2', b'Summer Term(II Year)'), (b'ST3', b'Summer Term(III Year)'), (b'ST4', b'Summer Term(IV Year)'), (b'PG10', b'PG(I Year I Semester)'), (b'PG11', b'PG(I Year II Semester)'), (b'PG20', b'PG(II Year I Semester)'), (b'PG21', b'PG(II Year II Semester)'), (b'PG30', b'PG(III Year I Semester)'), (b'PG31', b'PG(III Year II Semester)'), (b'PHD10', b'PHD(I Year I Semester)'), (b'PHD11', b'PHD(I Year II Semester)'), (b'PHD20', b'PHD(II Year I Semester)'), (b'PHD21', b'PHD(II Year II Semester)'), (b'PHD30', b'PHD(III Year I Semester)'), (b'PHD31', b'PHD(III Year II Semester)'), (b'PHD40', b'PHD(IV Year I Semester)'), (b'PHD41', b'PHD(IV Year II Semester)'), (b'PHD50', b'PHD(V Year I Semester)'), (b'PHD51', b'PHD(V Year II Semester)'), (b'PHD60', b'PHD(VI Year I Semester)'), (b'PHD61', b'PHD(VI Year II Semester)'), (b'PHD70', b'PHD(VII Year I Semester)'), (b'PHD71', b'PHD(VII Year II Semester)'), (b'PHD80', b'PHD(VIII Year I Semester)'), (b'PHD81', b'PHD(VIII Year II Semester)'), (b'PHD90', b'PHD(IX Year I Semester)'), (b'PHD91', b'PHD(IX Year II Semester)'), (b'PHD0', b'PHD Overall'), (b'UG00', b'UG(New Entrants)')])),
                ('subject_area', models.CharField(max_length=10, choices=[(b'DCC', b'Departmental Core Course'), (b'IEC', b'Institute Elective Course'), (b'DEC', b'Departmental Elective Course'), (b'PEC', b'Programme Elective Course'), (b'OEC', b'Open Elective Course'), (b'ICC', b'Institute Core Course'), (b'RP', b'Project'), (b'SEM', b'Seminar'), (b'PHDNPRE', b'PHD Non Prescribed Course'), (b'PRO', b'Proficiency')])),
                ('group_status', models.BooleanField(default=False)),
                ('branch', models.ForeignKey(to='nucleus.Branch')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstituteElectives',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('semester', models.CharField(max_length=100, choices=[(b'UG0', b'UG Overall'), (b'DPLM', b'Diploma'), (b'PG0', b'PG Overall'), (b'10TH', b'Tenth'), (b'12TH', b'Twelfth'), (b'UG10', b'UG(I Year I Semester)'), (b'UG11', b'UG(I Year II Semester)'), (b'UG20', b'UG(II Year I Semester)'), (b'UG21', b'UG(II Year II Semester)'), (b'UG30', b'UG(III Year I Semester)'), (b'UG31', b'UG(III Year II Semester)'), (b'UG40', b'UG(IV Year I Semester)'), (b'UG41', b'UG(IV Year II Semester)'), (b'UG50', b'UG(V Year I Semester)'), (b'UG51', b'UG(V Year II Semester)'), (b'ST1', b'Summer Term(I Year)'), (b'ST2', b'Summer Term(II Year)'), (b'ST3', b'Summer Term(III Year)'), (b'ST4', b'Summer Term(IV Year)'), (b'PG10', b'PG(I Year I Semester)'), (b'PG11', b'PG(I Year II Semester)'), (b'PG20', b'PG(II Year I Semester)'), (b'PG21', b'PG(II Year II Semester)'), (b'PG30', b'PG(III Year I Semester)'), (b'PG31', b'PG(III Year II Semester)'), (b'PHD10', b'PHD(I Year I Semester)'), (b'PHD11', b'PHD(I Year II Semester)'), (b'PHD20', b'PHD(II Year I Semester)'), (b'PHD21', b'PHD(II Year II Semester)'), (b'PHD30', b'PHD(III Year I Semester)'), (b'PHD31', b'PHD(III Year II Semester)'), (b'PHD40', b'PHD(IV Year I Semester)'), (b'PHD41', b'PHD(IV Year II Semester)'), (b'PHD50', b'PHD(V Year I Semester)'), (b'PHD51', b'PHD(V Year II Semester)'), (b'PHD60', b'PHD(VI Year I Semester)'), (b'PHD61', b'PHD(VI Year II Semester)'), (b'PHD70', b'PHD(VII Year I Semester)'), (b'PHD71', b'PHD(VII Year II Semester)'), (b'PHD80', b'PHD(VIII Year I Semester)'), (b'PHD81', b'PHD(VIII Year II Semester)'), (b'PHD90', b'PHD(IX Year I Semester)'), (b'PHD91', b'PHD(IX Year II Semester)'), (b'PHD0', b'PHD Overall'), (b'UG00', b'UG(New Entrants)')])),
                ('choice_list', models.CharField(max_length=100)),
                ('tentative_elective', models.CharField(max_length=100)),
                ('group_code', models.CharField(max_length=10)),
                ('student', models.ForeignKey(to='nucleus.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstituteElectivesNotEligibleMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('branch', models.ForeignKey(to='nucleus.Branch')),
                ('course_details', models.ForeignKey(to='regol.CourseDetails')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JeeEntrants',
            fields=[
                ('enrollment_no', models.CharField(max_length=10, unique=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('admission_year', models.CharField(max_length=4)),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('fathers_name', models.CharField(max_length=100, verbose_name=b"Father's Name")),
                ('birth_date', models.DateField(verbose_name=b'Date of Birth')),
                ('rank', models.PositiveIntegerField()),
                ('nationality', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=3, choices=[(b'GEN', b'General'), (b'SC', b'Scheduled Caste'), (b'ST', b'Scheduled Tribe'), (b'OBC', b'Other Backward Classes')])),
                ('registration_no', models.CharField(max_length=100, null=True, blank=True)),
                ('category_rank', models.PositiveIntegerField(null=True, blank=True)),
                ('received_fee', models.BooleanField(default=False)),
                ('registered', models.BooleanField(default=False)),
                ('branch', models.ForeignKey(to='nucleus.Branch')),
            ],
            options={
                'ordering': ['branch', 'enrollment_no'],
                'verbose_name': 'JEE Entrants',
                'verbose_name_plural': 'JEE Entrants',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhdInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('internal_guide_1', models.CharField(max_length=100, blank=True)),
                ('internal_guide_2', models.CharField(max_length=100, blank=True)),
                ('initial_regn_date', models.DateField(null=True, blank=True)),
                ('external_guide', models.CharField(max_length=100, blank=True)),
                ('thesis_topic', models.CharField(max_length=100, blank=True)),
                ('thesis_abstract', models.TextField(blank=True)),
                ('time_type', models.CharField(blank=True, max_length=100, choices=[(b'FULL', b'Fulltime'), (b'PART', b'Parttime')])),
                ('scheme', models.CharField(blank=True, max_length=100, choices=[(b'MHRD', b'MHRD')])),
                ('mhrd_asst_comp_date', models.DateField(null=True, blank=True)),
                ('student', models.OneToOneField(to='nucleus.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegisteredCourses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('credits', models.IntegerField()),
                ('registered_date', models.DateField()),
                ('semester', models.CharField(max_length=100, choices=[(b'UG0', b'UG Overall'), (b'DPLM', b'Diploma'), (b'PG0', b'PG Overall'), (b'10TH', b'Tenth'), (b'12TH', b'Twelfth'), (b'UG10', b'UG(I Year I Semester)'), (b'UG11', b'UG(I Year II Semester)'), (b'UG20', b'UG(II Year I Semester)'), (b'UG21', b'UG(II Year II Semester)'), (b'UG30', b'UG(III Year I Semester)'), (b'UG31', b'UG(III Year II Semester)'), (b'UG40', b'UG(IV Year I Semester)'), (b'UG41', b'UG(IV Year II Semester)'), (b'UG50', b'UG(V Year I Semester)'), (b'UG51', b'UG(V Year II Semester)'), (b'ST1', b'Summer Term(I Year)'), (b'ST2', b'Summer Term(II Year)'), (b'ST3', b'Summer Term(III Year)'), (b'ST4', b'Summer Term(IV Year)'), (b'PG10', b'PG(I Year I Semester)'), (b'PG11', b'PG(I Year II Semester)'), (b'PG20', b'PG(II Year I Semester)'), (b'PG21', b'PG(II Year II Semester)'), (b'PG30', b'PG(III Year I Semester)'), (b'PG31', b'PG(III Year II Semester)'), (b'PHD10', b'PHD(I Year I Semester)'), (b'PHD11', b'PHD(I Year II Semester)'), (b'PHD20', b'PHD(II Year I Semester)'), (b'PHD21', b'PHD(II Year II Semester)'), (b'PHD30', b'PHD(III Year I Semester)'), (b'PHD31', b'PHD(III Year II Semester)'), (b'PHD40', b'PHD(IV Year I Semester)'), (b'PHD41', b'PHD(IV Year II Semester)'), (b'PHD50', b'PHD(V Year I Semester)'), (b'PHD51', b'PHD(V Year II Semester)'), (b'PHD60', b'PHD(VI Year I Semester)'), (b'PHD61', b'PHD(VI Year II Semester)'), (b'PHD70', b'PHD(VII Year I Semester)'), (b'PHD71', b'PHD(VII Year II Semester)'), (b'PHD80', b'PHD(VIII Year I Semester)'), (b'PHD81', b'PHD(VIII Year II Semester)'), (b'PHD90', b'PHD(IX Year I Semester)'), (b'PHD91', b'PHD(IX Year II Semester)'), (b'PHD0', b'PHD Overall'), (b'UG00', b'UG(New Entrants)')])),
                ('subject_area', models.CharField(max_length=10)),
                ('cleared_status', models.CharField(default=b'NXT', max_length=10, choices=[(b'CUR', b'Current'), (b'CLR', b'Cleared'), (b'NXT', b'Next'), (b'DRP', b'Dropped'), (b'BCK', b'Back')])),
                ('grade', models.CharField(default=b'-', max_length=2, choices=[(b'A+', b'10'), (b'A', b'9'), (b'B+', b'8'), (b'B', b'7'), (b'C+', b'6'), (b'C', b'5'), (b'D', b'4'), (b'F', b'Back'), (b'-', b'NA')])),
                ('group_code', models.CharField(default=b'-1', max_length=10)),
                ('course_details', models.ForeignKey(to='regol.CourseDetails')),
                ('student', models.ForeignKey(to='nucleus.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegolStudent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reg_type', models.CharField(default=b'RFN', max_length=100, choices=[(b'IER', b'Institute Elective Registration'), (b'DER', b'Departmental Elective Registration'), (b'SBR', b'Subject Registration'), (b'SMR', b'Semester Registration'), (b'RFN', b'Registration Finalized')])),
                ('semreg_finalized', models.BooleanField(default=False)),
                ('student', models.OneToOneField(to='nucleus.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
