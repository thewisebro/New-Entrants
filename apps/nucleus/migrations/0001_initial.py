# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import crop_image.base
import core.models.fields
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('photo', crop_image.base.CropImageModelField(upload_to=b'nucleus/photo/', blank=True)),
                ('gender', models.CharField(blank=True, max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('birth_date', core.models.fields.DateField(null=True, verbose_name=b'Date of Birth', blank=True)),
                ('contact_no', models.CharField(max_length=12, verbose_name=b'Contact No', blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Alumni',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('admission_year', models.IntegerField()),
                ('cgpa', models.CharField(max_length=6, blank=True)),
                ('passout_year', models.IntegerField(null=True, blank=True)),
                ('address', models.CharField(max_length=100, blank=True)),
                ('pincode', models.CharField(max_length=10, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('degree', models.CharField(max_length=10, choices=[(b'B.Tech.', b'Bachelor of Technology'), (b'B.Arch.', b'Bachelor of Architecture'), (b'IDD', b'Integrated Dual Degree'), (b'M.Tech.', b'Master of Technology'), (b'IMT', b'Integrated Master of Technology'), (b'IMSc', b'Integrated Master of Science'), (b'M.Arch.', b'Master of Architecture'), (b'MURP', b'Master of Urban and Regional Planning'), (b'PGDip', b'Postgraduate Diploma Course'), (b'MBA', b'Master of Business Administration'), (b'MCA', b'Master of Computer Applications'), (b'MSc', b'Master of Sciences'), (b'PHD', b'Doctor of Philosophy')])),
                ('department', models.CharField(max_length=10, choices=[(b'AHEC', b'Alternate Hydro Energy Centre'), (b'ASED', b'Applied Science and Engineering Department'), (b'CNT', b'Centre for Nanotechnology'), (b'ARCD', b'Architecture and Planning Department'), (b'BTD', b'Biotechnology Department'), (b'CHED', b'Chemical Engineering Department'), (b'CDM', b'Centre of Excellence in Disaster Mitigation and Management'), (b'CYD', b'Chemistry Department'), (b'CED', b'Civil Engineering Department'), (b'CSED', b'Computer Science and Engineering Department'), (b'CT', b'Centre for Transportation Systems'), (b'EQD', b'Earthquake Department'), (b'ESD', b'Earth Sciences Department'), (b'EED', b'Electrical Engineering Department'), (b'ECED', b'Electronics and Communication Engineering Department'), (b'HSD', b'Humanities and Social Sciences Department'), (b'HYD', b'Hydrology Department'), (b'MSD', b'Management Studies Department'), (b'MAD', b'Mathematics Department'), (b'MIED', b'Mechanical and Industrial Engineering Department'), (b'MMED', b'Metallurgical and Materials Engineering Department'), (b'PTD', b'Paper Technology Department'), (b'PPED', b'Polymer and Process Engineering Department'), (b'PHD', b'Physics Department'), (b'WRDMD', b'Water Resources Development and Management Department'), (b'CDM', b'Centre for Disaster Mitigation'), (b'ICC', b'Institute Computer Centre'), (b'IIC', b'Institute Instrumentation Centre'), (b'QIP', b'Quality Improvement Programme')])),
                ('graduation', models.CharField(max_length=10, choices=[(b'UG', b'Under Graduate'), (b'PG', b'Post Graduate'), (b'PHD', b'PhD')])),
                ('no_of_semesters', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Branches',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(1, b'FRIEND'), (2, b'UNFRIEND'), (3, b'BLOCK')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('id', models.CharField(max_length=15, serialize=False, primary_key=True)),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('credits', models.IntegerField()),
                ('subject_area', models.CharField(max_length=10)),
                ('semtype', models.CharField(max_length=1, choices=[(b'S', b'Spring'), (b'A', b'Autumn')])),
                ('year', models.IntegerField()),
                ('seats', models.PositiveIntegerField(null=True, blank=True)),
                ('pre_requisites', models.ManyToManyField(to='nucleus.Course', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('department', models.CharField(max_length=10, choices=[(b'AHEC', b'Alternate Hydro Energy Centre'), (b'ASED', b'Applied Science and Engineering Department'), (b'CNT', b'Centre for Nanotechnology'), (b'ARCD', b'Architecture and Planning Department'), (b'BTD', b'Biotechnology Department'), (b'CHED', b'Chemical Engineering Department'), (b'CDM', b'Centre of Excellence in Disaster Mitigation and Management'), (b'CYD', b'Chemistry Department'), (b'CED', b'Civil Engineering Department'), (b'CSED', b'Computer Science and Engineering Department'), (b'CT', b'Centre for Transportation Systems'), (b'EQD', b'Earthquake Department'), (b'ESD', b'Earth Sciences Department'), (b'EED', b'Electrical Engineering Department'), (b'ECED', b'Electronics and Communication Engineering Department'), (b'HSD', b'Humanities and Social Sciences Department'), (b'HYD', b'Hydrology Department'), (b'MSD', b'Management Studies Department'), (b'MAD', b'Mathematics Department'), (b'MIED', b'Mechanical and Industrial Engineering Department'), (b'MMED', b'Metallurgical and Materials Engineering Department'), (b'PTD', b'Paper Technology Department'), (b'PPED', b'Polymer and Process Engineering Department'), (b'PHD', b'Physics Department'), (b'WRDMD', b'Water Resources Development and Management Department'), (b'CDM', b'Centre for Disaster Mitigation'), (b'ICC', b'Institute Computer Centre'), (b'IIC', b'Institute Instrumentation Centre'), (b'QIP', b'Quality Improvement Programme')])),
                ('resume', models.FileField(null=True, upload_to=b'facapp/resumes', blank=True)),
                ('designation', models.CharField(max_length=10, choices=[(b'HOD', b'Head Of Department'), (b'HOC', b'Head Of Centre'), (b'EP', b'Emeritus Professor'), (b'GF', b'Guest Faculty'), (b'WS', b'Workshop Superintendent'), (b'AWS', b'Assistant Workshop Superintendent'), (b'RF', b'Retired Faculty'), (b'SP', b'System Programmer'), (b'PRO', b'Professor'), (b'LEC', b'Lecturar'), (b'VS', b'Visiting Scientist'), (b'VP', b'Visiting Professor'), (b'SO', b'Scientific Officer'), (b'AP', b'Assistant Professor'), (b'CSO', b'Chief Scientific Officer'), (b'CP', b'Chair Professor'), (b'SSO', b'Senior Scientific Officer'), (b'JP', b'Joint Professor'), (b'ASP', b'Associate Professor'), (b'EF', b'Ex Faculty'), (b'EMF', b'Emeritus Fellows'), (b'APC', b'Assistant Professor (Contract)')])),
                ('address', models.CharField(max_length=100, null=True, blank=True)),
                ('employee_code', models.CharField(max_length=10, blank=True)),
                ('date_of_joining', models.CharField(max_length=10, null=True, blank=True)),
                ('home_page', models.URLField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Faculties',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('is_declined', models.BooleanField(default=False)),
                ('is_seen', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GlobalVar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IntroAd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PHPSession',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('session_key', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('session_data', models.TextField()),
                ('expire_date', core.models.fields.DateTimeField(db_index=True)),
                ('username', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'nucleus_php_session',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegisteredBranchCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('semester_no', models.IntegerField()),
                ('subject_area', models.CharField(max_length=10, blank=True)),
                ('credits', models.IntegerField(null=True, blank=True)),
                ('branch', models.ForeignKey(to='nucleus.Branch')),
                ('course', models.ForeignKey(to='nucleus.Course')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegisteredCourseChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('subject_area', models.CharField(max_length=10, blank=True)),
                ('credits', models.IntegerField(null=True, blank=True)),
                ('change', models.CharField(max_length=3, choices=[(b'ADD', b'Course Added'), (b'DRP', b'Course Dropped')])),
                ('backlog_registeredcoursechange', models.ForeignKey(related_name=b'next_registeredcoursechange', blank=True, to='nucleus.RegisteredCourseChange', null=True)),
                ('course', models.ForeignKey(to='nucleus.Course')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegisteredCourseChangeAlumni',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('subject_area', models.CharField(max_length=10, blank=True)),
                ('credits', models.IntegerField(null=True, blank=True)),
                ('change', models.CharField(max_length=3, choices=[(b'ADD', b'Course Added'), (b'DRP', b'Course Dropped')])),
                ('backlog_registeredcoursechangealumni', models.ForeignKey(related_name=b'next_registeredcoursechangealumni', blank=True, to='nucleus.RegisteredCourseChangeAlumni', null=True)),
                ('course', models.ForeignKey(to='nucleus.Course')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('semester', models.CharField(max_length=10, choices=[(b'UG0', b'UG Overall'), (b'DPLM', b'Diploma'), (b'PG0', b'PG Overall'), (b'10TH', b'Tenth'), (b'12TH', b'Twelfth'), (b'UG10', b'UG(I Year I Semester)'), (b'UG11', b'UG(I Year II Semester)'), (b'UG20', b'UG(II Year I Semester)'), (b'UG21', b'UG(II Year II Semester)'), (b'UG30', b'UG(III Year I Semester)'), (b'UG31', b'UG(III Year II Semester)'), (b'UG40', b'UG(IV Year I Semester)'), (b'UG41', b'UG(IV Year II Semester)'), (b'UG50', b'UG(V Year I Semester)'), (b'UG51', b'UG(V Year II Semester)'), (b'ST1', b'Summer Term(I Year)'), (b'ST2', b'Summer Term(II Year)'), (b'ST3', b'Summer Term(III Year)'), (b'ST4', b'Summer Term(IV Year)'), (b'PG10', b'PG(I Year I Semester)'), (b'PG11', b'PG(I Year II Semester)'), (b'PG20', b'PG(II Year I Semester)'), (b'PG21', b'PG(II Year II Semester)'), (b'PG30', b'PG(III Year I Semester)'), (b'PG31', b'PG(III Year II Semester)'), (b'PHD10', b'PHD(I Year I Semester)'), (b'PHD11', b'PHD(I Year II Semester)'), (b'PHD20', b'PHD(II Year I Semester)'), (b'PHD21', b'PHD(II Year II Semester)'), (b'PHD30', b'PHD(III Year I Semester)'), (b'PHD31', b'PHD(III Year II Semester)'), (b'PHD40', b'PHD(IV Year I Semester)'), (b'PHD41', b'PHD(IV Year II Semester)'), (b'PHD50', b'PHD(V Year I Semester)'), (b'PHD51', b'PHD(V Year II Semester)'), (b'PHD60', b'PHD(VI Year I Semester)'), (b'PHD61', b'PHD(VI Year II Semester)'), (b'PHD70', b'PHD(VII Year I Semester)'), (b'PHD71', b'PHD(VII Year II Semester)'), (b'PHD80', b'PHD(VIII Year I Semester)'), (b'PHD81', b'PHD(VIII Year II Semester)'), (b'PHD90', b'PHD(IX Year I Semester)'), (b'PHD91', b'PHD(IX Year II Semester)'), (b'PHD0', b'PHD Overall'), (b'UG00', b'UG(New Entrants)')])),
                ('semester_no', models.IntegerField()),
                ('admission_year', models.IntegerField(verbose_name=b'Admission Year')),
                ('admission_semtype', models.CharField(max_length=1, verbose_name=b'Admission Semester', choices=[(b'S', b'Spring'), (b'A', b'Autumn')])),
                ('cgpa', models.CharField(max_length=6, blank=True)),
                ('bhawan', models.CharField(default=None, max_length=10, null=True, blank=True, choices=[(b'AZB', b'Azad Bhawan'), (b'CTB', b'Cautley Bhawan'), (b'GNB', b'Ganga Bhawan'), (b'GVB', b'Govind Bhawan'), (b'JWB', b'Jawahar Bhawan'), (b'RKB', b'Radhakrishnan Bhawan'), (b'RJB', b'Rajendra Bhawan'), (b'RGB', b'Rajiv Bhawan'), (b'RVB', b'Ravindra Bhawan'), (b'MVB', b'Malviya Bhawan'), (b'SB', b'Sarojini Bhawan'), (b'KB', b'Kasturba Bhawan'), (b'IB', b' Indra Bhawan')])),
                ('room_no', models.CharField(max_length=10, verbose_name=b'Room No', blank=True)),
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StudentAlumni',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('semester', models.CharField(max_length=10, choices=[(b'UG0', b'UG Overall'), (b'DPLM', b'Diploma'), (b'PG0', b'PG Overall'), (b'10TH', b'Tenth'), (b'12TH', b'Twelfth'), (b'UG10', b'UG(I Year I Semester)'), (b'UG11', b'UG(I Year II Semester)'), (b'UG20', b'UG(II Year I Semester)'), (b'UG21', b'UG(II Year II Semester)'), (b'UG30', b'UG(III Year I Semester)'), (b'UG31', b'UG(III Year II Semester)'), (b'UG40', b'UG(IV Year I Semester)'), (b'UG41', b'UG(IV Year II Semester)'), (b'UG50', b'UG(V Year I Semester)'), (b'UG51', b'UG(V Year II Semester)'), (b'ST1', b'Summer Term(I Year)'), (b'ST2', b'Summer Term(II Year)'), (b'ST3', b'Summer Term(III Year)'), (b'ST4', b'Summer Term(IV Year)'), (b'PG10', b'PG(I Year I Semester)'), (b'PG11', b'PG(I Year II Semester)'), (b'PG20', b'PG(II Year I Semester)'), (b'PG21', b'PG(II Year II Semester)'), (b'PG30', b'PG(III Year I Semester)'), (b'PG31', b'PG(III Year II Semester)'), (b'PHD10', b'PHD(I Year I Semester)'), (b'PHD11', b'PHD(I Year II Semester)'), (b'PHD20', b'PHD(II Year I Semester)'), (b'PHD21', b'PHD(II Year II Semester)'), (b'PHD30', b'PHD(III Year I Semester)'), (b'PHD31', b'PHD(III Year II Semester)'), (b'PHD40', b'PHD(IV Year I Semester)'), (b'PHD41', b'PHD(IV Year II Semester)'), (b'PHD50', b'PHD(V Year I Semester)'), (b'PHD51', b'PHD(V Year II Semester)'), (b'PHD60', b'PHD(VI Year I Semester)'), (b'PHD61', b'PHD(VI Year II Semester)'), (b'PHD70', b'PHD(VII Year I Semester)'), (b'PHD71', b'PHD(VII Year II Semester)'), (b'PHD80', b'PHD(VIII Year I Semester)'), (b'PHD81', b'PHD(VIII Year II Semester)'), (b'PHD90', b'PHD(IX Year I Semester)'), (b'PHD91', b'PHD(IX Year II Semester)'), (b'PHD0', b'PHD Overall'), (b'UG00', b'UG(New Entrants)')])),
                ('semester_no', models.IntegerField()),
                ('admission_year', models.IntegerField(verbose_name=b'Admission Year')),
                ('admission_semtype', models.CharField(max_length=1, verbose_name=b'Admission Semester', choices=[(b'S', b'Spring'), (b'A', b'Autumn')])),
                ('cgpa', models.CharField(max_length=6, blank=True)),
                ('bhawan', models.CharField(default=None, max_length=10, null=True, blank=True, choices=[(b'AZB', b'Azad Bhawan'), (b'CTB', b'Cautley Bhawan'), (b'GNB', b'Ganga Bhawan'), (b'GVB', b'Govind Bhawan'), (b'JWB', b'Jawahar Bhawan'), (b'RKB', b'Radhakrishnan Bhawan'), (b'RJB', b'Rajendra Bhawan'), (b'RGB', b'Rajiv Bhawan'), (b'RVB', b'Ravindra Bhawan'), (b'MVB', b'Malviya Bhawan'), (b'SB', b'Sarojini Bhawan'), (b'KB', b'Kasturba Bhawan'), (b'IB', b' Indra Bhawan')])),
                ('room_no', models.CharField(max_length=10, verbose_name=b'Room No', blank=True)),
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('fathers_name', models.CharField(max_length=100, verbose_name=b"Father's Name", blank=True)),
                ('fathers_occupation', models.CharField(max_length=100, verbose_name=b"Father's Occupation", blank=True)),
                ('fathers_office_address', models.CharField(max_length=100, verbose_name=b"Father's Office Address", blank=True)),
                ('fathers_office_phone_no', models.CharField(max_length=12, verbose_name=b"Father's Office Phone No", blank=True)),
                ('mothers_name', models.CharField(max_length=100, verbose_name=b"Mother's Name", blank=True)),
                ('permanent_address', models.CharField(max_length=100, verbose_name=b'Permanent Address', blank=True)),
                ('home_contact_no', models.CharField(max_length=12, verbose_name=b'Home Contact No', blank=True)),
                ('state', models.CharField(blank=True, max_length=3, choices=[(b'ADP', b'Andhra Pradesh'), (b'ARP', b'Arunachal Pradesh'), (b'ASM', b'Assam'), (b'BHR', b'Bihar'), (b'CHG', b'Chhattisgarh'), (b'DEL', b'Delhi'), (b'GOA', b'Goa'), (b'GUJ', b'Gujarat'), (b'HAR', b'Haryana'), (b'HMP', b'Himachal Pradesh'), (b'JNK', b'Jammu and Kashmir'), (b'JHK', b'Jharkhand'), (b'KAR', b'Karnataka'), (b'KRL', b'Kerala'), (b'MDP', b'Madya Pradesh'), (b'MAH', b'Maharashtra'), (b'MNP', b'Manipur'), (b'MGY', b'Meghalaya'), (b'MIZ', b'Mizoram'), (b'NGL', b'Nagaland'), (b'ORS', b'Orissa'), (b'PJB', b'Punjab'), (b'RAJ', b'Rajasthan'), (b'SIK', b'Sikkim'), (b'TAN', b'Tamil Nadu'), (b'TLG', b'Telangana'), (b'TRP', b'Tripura'), (b'UTA', b'Uttaranchal'), (b'UTP', b'Uttar Pradesh'), (b'WSB', b'West Bengal')])),
                ('city', models.CharField(max_length=100, blank=True)),
                ('pincode', models.CharField(max_length=10, blank=True)),
                ('bank_name', models.CharField(max_length=100, verbose_name=b'Bank Name', blank=True)),
                ('bank_account_no', models.CharField(max_length=25, verbose_name=b'Bank Account No', blank=True)),
                ('passport_no', models.CharField(max_length=25, verbose_name=b'Passport No', blank=True)),
                ('nearest_station', models.CharField(blank=True, max_length=100, verbose_name=b'Nearest Station', choices=[(b'ABR', b'ABU ROAD - ABR'), (b'AGC', b'AGRA CANTT - AGC'), (b'AF', b'AGRA FORT - AF'), (b'AGA', b'AGRA CITY - AGA'), (b'ADI', b'AHMEDABAD JN - ADI'), (b'AII', b'AJMER - AII'), (b'AK', b'AKOLA - AK'), (b'ALJN', b'ALIGARH JN - ALJN'), (b'ALD', b'ALLAHABAD - ALD'), (b'ALLP', b'ALLEPPEY - ALLP'), (b'AWR', b'ALWAR - AWR'), (b'AWY', b'ALWAYE - AWY'), (b'UMB', b'AMBALA - UMB'), (b'AME', b'AMETHI - AME'), (b'AMI', b'AMRAVATI - AMI'), (b'ASR', b'AMRITSAR - ASR'), (b'ASN', b'ASANSOL JN - ASN'), (b'AWB', b'AURANGABAD - AWB'), (b'AMH', b'AZAMGARH - AMH'), (b'BRK', b'BAHRAICH - BRK'), (b'SBC', b'BANGALORE - SBC'), (b'BUI', b'BALLIA - BUI'), (b'BWT', b'BANGARAPET - BWT'), (b'BP', b'BARRACKPORE - BP'), (b'BJU', b'BARAUNI JN - BJU'), (b'BE', b'BAREILLY - BE'), (b'BST', b'BASTI - BST'), (b'BSL', b'BHUSAVAL - BSL'), (b'BGS', b'BEGU SARAI - BGS'), (b'BGM', b'BELGAUM - BGM'), (b'BAY', b'BELLARY - BAY'), (b'BGP', b'BHAGALPUR - BGP'), (b'BKN', b'BIKANER JN - BKN'), (b'BSP', b'BILASPUR - BSP'), (b'BINA', b'BINA - BINA'), (b'BPL', b'BHOPAL - BPL'), (b'BTI', b'BHATINDA - BTI'), (b'BKSC', b'BOKARO STL CITY - BKSC'), (b'BBS', b'BHUBANESHWAR - BBS'), (b'BWN', b'BURDWAN - BWN'), (b'BXR', b'BUXAR - BXR'), (b'CLT', b'CALICUT - CLT'), (b'CDG', b'CHANDIGARH - CDG'), (b'MAS', b'CHENNAI - MAS'), (b'CHTS', b'COCHIN - CHTS'), (b'CRJ', b'CHITTARANJAN - CRJ'), (b'CBE', b'COIMBATORE JN - CBE'), (b'DBG', b'DARBHANGA JN - DBG'), (b'DJ', b'DARJEELING - DJ'), (b'DDN', b'DEHRADUN - DDN'), (b'DHN', b'DHANBAD JN - DHN'), (b'DWR', b'DHARWAR - DWR'), (b'DURG', b'DURG - DURG'), (b'DBRT', b'DIBRUGARH TOWN - DBRT'), (b'ERS', b'ERNAKULAM - ERS'), (b'ED', b'ERODE - ED'), (b'FD', b'FAIZABAD JN - FD'), (b'FDB', b'FARIDABAD - FDB'), (b'FBD', b'FARUKHABAD - FBD'), (b'GAYA', b'GAYA JN - GAYA'), (b'G', b'GONDIA - G'), (b'GKP', b'GORAKHPUR JN - GKP'), (b'GR', b'GULBARGA - GR'), (b'GNT', b'GUNTUR - GNT'), (b'GHY', b'GUWAHATI - GHY'), (b'GWL', b'GWALIOR - GWL'), (b'HBJ', b'HABIBGANJ - HBJ'), (b'HWH', b'HOWRAH - HWH'), (b'HYB', b'HYDERABAD - HYB'), (b'INDB', b'INDORE JN BG - INDB'), (b'ET', b'ITARSI - ET'), (b'JBP', b'JABALPUR - JBP'), (b'JP', b'JAIPUR - JP'), (b'JSM', b'JAISALMER - JSM'), (b'JUC', b'JALANDHAR CITY - JUC'), (b'JAT', b'JAMMU - JAT'), (b'JHS', b'JHANSI JN - JHS'), (b'JU', b'JODHPUR - JU'), (b'KLK', b'KALKA - KLK'), (b'CNB', b'KANPUR - CNB'), (b'CAPE', b'KANYAKUMARI - CAPE'), (b'KGM', b'KATHGODAM - KGM'), (b'KPD', b'KATPADI - KPD'), (b'HWH', b'KOLKATA - HWH'), (b'KOTA', b'KOTA JN - KOTA'), (b'KZJ', b'KAZIPET - KZJ'), (b'LKO', b'LUCKNOW - LKO'), (b'LDH', b'LUDHIANA - LDH'), (b'MAO', b'MADGAON - MAO'), (b'MDU', b'MADURAI - MDU'), (b'MMC', b'MAHAMANDIR - MMC'), (b'MAQ', b'MANGALORE - MAQ'), (b'MMR', b'MANMAD - MMR'), (b'MTJ', b'MATHURA JN - MTJ'), (b'MAU', b'MAU JN - MAU'), (b'MTC', b'MEERUT CITY - MTC'), (b'MB', b'MORADABAD - MB'), (b'MGS', b'MUGHAL SARAI - MGS'), (b'BCT', b'MUMBAI - BCT'), (b'MYS', b'MYSORE - MYS'), (b'NGP', b'NAGPUR - NGP'), (b'NK', b'NASIK - NK'), (b'NLR', b'NELLORE - NLR'), (b'NJP', b'NEW JALPAIGURI - NJP'), (b'NDLS', b'NEW DELHI - NDLS'), (b'PGT', b'PALGHAT - PGT'), (b'PNP', b'PANIPAT JN - PNP'), (b'PTA', b'PATIALA - PTA'), (b'PNBE', b'PATNA JN - PNBE'), (b'PUNE', b'PUNE JN - PUNE'), (b'RBL', b'RAE BARELI JN - RBL'), (b'RIG', b'RAIGARH - RIG'), (b'R', b'RAIPUR - R'), (b'RMM', b'RAMESWARAM - RMM'), (b'RNC', b'RANCHI - RNC'), (b'RRME', b'RANCHI ROAD - RRME'), (b'RTM', b'RATLAM - RTM'), (b'RN', b'RATNAGIRI - RN'), (b'REWA', b'REWA - REWA'), (b'ROK', b'ROHTAK - ROK'), (b'RKSH', b'RISHIKESH - RKSH'), (b'RK', b'ROORKEE - RK'), (b'ROU', b'ROURKELA - ROU'), (b'SRE', b'SAHARANPUR - SRE'), (b'SA', b'SALEM - SA'), (b'SLI', b'SANGLI - SLI'), (b'STA', b'SATNA - STA'), (b'SNP', b'SONIPAT - SNP'), (b'SCL', b'SILCHAR - SCL'), (b'SML', b'SIMLA - SML'), (b'SVKS', b'SIVAKASI - SVKS'), (b'ST', b'SURAT - ST'), (b'TATA', b'TATANAGAR JN - TATA'), (b'TNA', b'THANE - TNA'), (b'TJ', b'THANJAVUR - TJ'), (b'TPTY', b'TIRUPATI - TPTY'), (b'TPJ', b'TIRUCHIRAPALLI - TPJ'), (b'TCR', b'TRICHUR - TCR'), (b'TVC', b'TRIVANDRUM - TVC'), (b'TN', b'TUTICORIN - TN'), (b'UDZ', b'UDAIPUR - UDZ'), (b'UJN', b'UJJAIN - UJN'), (b'BRC', b'VADODARA - BRC'), (b'BSB', b'VARANASI JN - BSB'), (b'VSG', b'VASCO DA GAMA - VSG'), (b'BZA', b'VIJAYAWADA JN - BZA'), (b'VSKP', b'VISHAKAPATNAM - VSKP'), (b'WL', b'WARANGAL - WL'), (b'WR', b'WARDHA - WR')])),
                ('local_guardian_name', models.CharField(max_length=100, verbose_name=b"Local Guardian's Name", blank=True)),
                ('local_guardian_address', models.CharField(max_length=100, verbose_name=b"Local Guardian's Address", blank=True)),
                ('local_guardian_contact_no', models.CharField(max_length=12, verbose_name=b"Local Guardian's Contact No", blank=True)),
                ('category', models.CharField(blank=True, max_length=3, choices=[(b'GEN', b'General'), (b'SC', b'Scheduled Caste'), (b'ST', b'Scheduled Tribe'), (b'OBC', b'Other Backward Classes')])),
                ('nationality', models.CharField(max_length=100, blank=True)),
                ('marital_status', models.CharField(blank=True, max_length=3, verbose_name=b'Marital Status', choices=[(b'SIN', b'Single'), (b'MAR', b'Married')])),
                ('blood_group', models.CharField(blank=True, max_length=3, verbose_name=b'Blood Group', choices=[(b'O+', b'O+'), (b'O-', b'O-'), (b'AB+', b'AB+'), (b'AB-', b'AB-'), (b'A+', b'A+'), (b'A-', b'A-'), (b'B+', b'B+'), (b'B-', b'B-')])),
                ('physically_disabled', models.BooleanField(default=False, verbose_name=b'Physically Disabled')),
                ('fulltime', models.BooleanField(default=False)),
                ('resident', models.BooleanField(default=True)),
                ('license_no', models.CharField(max_length=100, verbose_name=b'License No', blank=True)),
                ('student', models.OneToOneField(primary_key=True, serialize=False, to='nucleus.Student')),
            ],
            options={
                'verbose_name': 'Student Information',
                'verbose_name_plural': 'Students Information',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StudentInfoAlumni',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('fathers_name', models.CharField(max_length=100, verbose_name=b"Father's Name", blank=True)),
                ('fathers_occupation', models.CharField(max_length=100, verbose_name=b"Father's Occupation", blank=True)),
                ('fathers_office_address', models.CharField(max_length=100, verbose_name=b"Father's Office Address", blank=True)),
                ('fathers_office_phone_no', models.CharField(max_length=12, verbose_name=b"Father's Office Phone No", blank=True)),
                ('mothers_name', models.CharField(max_length=100, verbose_name=b"Mother's Name", blank=True)),
                ('permanent_address', models.CharField(max_length=100, verbose_name=b'Permanent Address', blank=True)),
                ('home_contact_no', models.CharField(max_length=12, verbose_name=b'Home Contact No', blank=True)),
                ('state', models.CharField(blank=True, max_length=3, choices=[(b'ADP', b'Andhra Pradesh'), (b'ARP', b'Arunachal Pradesh'), (b'ASM', b'Assam'), (b'BHR', b'Bihar'), (b'CHG', b'Chhattisgarh'), (b'DEL', b'Delhi'), (b'GOA', b'Goa'), (b'GUJ', b'Gujarat'), (b'HAR', b'Haryana'), (b'HMP', b'Himachal Pradesh'), (b'JNK', b'Jammu and Kashmir'), (b'JHK', b'Jharkhand'), (b'KAR', b'Karnataka'), (b'KRL', b'Kerala'), (b'MDP', b'Madya Pradesh'), (b'MAH', b'Maharashtra'), (b'MNP', b'Manipur'), (b'MGY', b'Meghalaya'), (b'MIZ', b'Mizoram'), (b'NGL', b'Nagaland'), (b'ORS', b'Orissa'), (b'PJB', b'Punjab'), (b'RAJ', b'Rajasthan'), (b'SIK', b'Sikkim'), (b'TAN', b'Tamil Nadu'), (b'TLG', b'Telangana'), (b'TRP', b'Tripura'), (b'UTA', b'Uttaranchal'), (b'UTP', b'Uttar Pradesh'), (b'WSB', b'West Bengal')])),
                ('city', models.CharField(max_length=100, blank=True)),
                ('pincode', models.CharField(max_length=10, blank=True)),
                ('bank_name', models.CharField(max_length=100, verbose_name=b'Bank Name', blank=True)),
                ('bank_account_no', models.CharField(max_length=25, verbose_name=b'Bank Account No', blank=True)),
                ('passport_no', models.CharField(max_length=25, verbose_name=b'Passport No', blank=True)),
                ('nearest_station', models.CharField(blank=True, max_length=100, verbose_name=b'Nearest Station', choices=[(b'ABR', b'ABU ROAD - ABR'), (b'AGC', b'AGRA CANTT - AGC'), (b'AF', b'AGRA FORT - AF'), (b'AGA', b'AGRA CITY - AGA'), (b'ADI', b'AHMEDABAD JN - ADI'), (b'AII', b'AJMER - AII'), (b'AK', b'AKOLA - AK'), (b'ALJN', b'ALIGARH JN - ALJN'), (b'ALD', b'ALLAHABAD - ALD'), (b'ALLP', b'ALLEPPEY - ALLP'), (b'AWR', b'ALWAR - AWR'), (b'AWY', b'ALWAYE - AWY'), (b'UMB', b'AMBALA - UMB'), (b'AME', b'AMETHI - AME'), (b'AMI', b'AMRAVATI - AMI'), (b'ASR', b'AMRITSAR - ASR'), (b'ASN', b'ASANSOL JN - ASN'), (b'AWB', b'AURANGABAD - AWB'), (b'AMH', b'AZAMGARH - AMH'), (b'BRK', b'BAHRAICH - BRK'), (b'SBC', b'BANGALORE - SBC'), (b'BUI', b'BALLIA - BUI'), (b'BWT', b'BANGARAPET - BWT'), (b'BP', b'BARRACKPORE - BP'), (b'BJU', b'BARAUNI JN - BJU'), (b'BE', b'BAREILLY - BE'), (b'BST', b'BASTI - BST'), (b'BSL', b'BHUSAVAL - BSL'), (b'BGS', b'BEGU SARAI - BGS'), (b'BGM', b'BELGAUM - BGM'), (b'BAY', b'BELLARY - BAY'), (b'BGP', b'BHAGALPUR - BGP'), (b'BKN', b'BIKANER JN - BKN'), (b'BSP', b'BILASPUR - BSP'), (b'BINA', b'BINA - BINA'), (b'BPL', b'BHOPAL - BPL'), (b'BTI', b'BHATINDA - BTI'), (b'BKSC', b'BOKARO STL CITY - BKSC'), (b'BBS', b'BHUBANESHWAR - BBS'), (b'BWN', b'BURDWAN - BWN'), (b'BXR', b'BUXAR - BXR'), (b'CLT', b'CALICUT - CLT'), (b'CDG', b'CHANDIGARH - CDG'), (b'MAS', b'CHENNAI - MAS'), (b'CHTS', b'COCHIN - CHTS'), (b'CRJ', b'CHITTARANJAN - CRJ'), (b'CBE', b'COIMBATORE JN - CBE'), (b'DBG', b'DARBHANGA JN - DBG'), (b'DJ', b'DARJEELING - DJ'), (b'DDN', b'DEHRADUN - DDN'), (b'DHN', b'DHANBAD JN - DHN'), (b'DWR', b'DHARWAR - DWR'), (b'DURG', b'DURG - DURG'), (b'DBRT', b'DIBRUGARH TOWN - DBRT'), (b'ERS', b'ERNAKULAM - ERS'), (b'ED', b'ERODE - ED'), (b'FD', b'FAIZABAD JN - FD'), (b'FDB', b'FARIDABAD - FDB'), (b'FBD', b'FARUKHABAD - FBD'), (b'GAYA', b'GAYA JN - GAYA'), (b'G', b'GONDIA - G'), (b'GKP', b'GORAKHPUR JN - GKP'), (b'GR', b'GULBARGA - GR'), (b'GNT', b'GUNTUR - GNT'), (b'GHY', b'GUWAHATI - GHY'), (b'GWL', b'GWALIOR - GWL'), (b'HBJ', b'HABIBGANJ - HBJ'), (b'HWH', b'HOWRAH - HWH'), (b'HYB', b'HYDERABAD - HYB'), (b'INDB', b'INDORE JN BG - INDB'), (b'ET', b'ITARSI - ET'), (b'JBP', b'JABALPUR - JBP'), (b'JP', b'JAIPUR - JP'), (b'JSM', b'JAISALMER - JSM'), (b'JUC', b'JALANDHAR CITY - JUC'), (b'JAT', b'JAMMU - JAT'), (b'JHS', b'JHANSI JN - JHS'), (b'JU', b'JODHPUR - JU'), (b'KLK', b'KALKA - KLK'), (b'CNB', b'KANPUR - CNB'), (b'CAPE', b'KANYAKUMARI - CAPE'), (b'KGM', b'KATHGODAM - KGM'), (b'KPD', b'KATPADI - KPD'), (b'HWH', b'KOLKATA - HWH'), (b'KOTA', b'KOTA JN - KOTA'), (b'KZJ', b'KAZIPET - KZJ'), (b'LKO', b'LUCKNOW - LKO'), (b'LDH', b'LUDHIANA - LDH'), (b'MAO', b'MADGAON - MAO'), (b'MDU', b'MADURAI - MDU'), (b'MMC', b'MAHAMANDIR - MMC'), (b'MAQ', b'MANGALORE - MAQ'), (b'MMR', b'MANMAD - MMR'), (b'MTJ', b'MATHURA JN - MTJ'), (b'MAU', b'MAU JN - MAU'), (b'MTC', b'MEERUT CITY - MTC'), (b'MB', b'MORADABAD - MB'), (b'MGS', b'MUGHAL SARAI - MGS'), (b'BCT', b'MUMBAI - BCT'), (b'MYS', b'MYSORE - MYS'), (b'NGP', b'NAGPUR - NGP'), (b'NK', b'NASIK - NK'), (b'NLR', b'NELLORE - NLR'), (b'NJP', b'NEW JALPAIGURI - NJP'), (b'NDLS', b'NEW DELHI - NDLS'), (b'PGT', b'PALGHAT - PGT'), (b'PNP', b'PANIPAT JN - PNP'), (b'PTA', b'PATIALA - PTA'), (b'PNBE', b'PATNA JN - PNBE'), (b'PUNE', b'PUNE JN - PUNE'), (b'RBL', b'RAE BARELI JN - RBL'), (b'RIG', b'RAIGARH - RIG'), (b'R', b'RAIPUR - R'), (b'RMM', b'RAMESWARAM - RMM'), (b'RNC', b'RANCHI - RNC'), (b'RRME', b'RANCHI ROAD - RRME'), (b'RTM', b'RATLAM - RTM'), (b'RN', b'RATNAGIRI - RN'), (b'REWA', b'REWA - REWA'), (b'ROK', b'ROHTAK - ROK'), (b'RKSH', b'RISHIKESH - RKSH'), (b'RK', b'ROORKEE - RK'), (b'ROU', b'ROURKELA - ROU'), (b'SRE', b'SAHARANPUR - SRE'), (b'SA', b'SALEM - SA'), (b'SLI', b'SANGLI - SLI'), (b'STA', b'SATNA - STA'), (b'SNP', b'SONIPAT - SNP'), (b'SCL', b'SILCHAR - SCL'), (b'SML', b'SIMLA - SML'), (b'SVKS', b'SIVAKASI - SVKS'), (b'ST', b'SURAT - ST'), (b'TATA', b'TATANAGAR JN - TATA'), (b'TNA', b'THANE - TNA'), (b'TJ', b'THANJAVUR - TJ'), (b'TPTY', b'TIRUPATI - TPTY'), (b'TPJ', b'TIRUCHIRAPALLI - TPJ'), (b'TCR', b'TRICHUR - TCR'), (b'TVC', b'TRIVANDRUM - TVC'), (b'TN', b'TUTICORIN - TN'), (b'UDZ', b'UDAIPUR - UDZ'), (b'UJN', b'UJJAIN - UJN'), (b'BRC', b'VADODARA - BRC'), (b'BSB', b'VARANASI JN - BSB'), (b'VSG', b'VASCO DA GAMA - VSG'), (b'BZA', b'VIJAYAWADA JN - BZA'), (b'VSKP', b'VISHAKAPATNAM - VSKP'), (b'WL', b'WARANGAL - WL'), (b'WR', b'WARDHA - WR')])),
                ('local_guardian_name', models.CharField(max_length=100, verbose_name=b"Local Guardian's Name", blank=True)),
                ('local_guardian_address', models.CharField(max_length=100, verbose_name=b"Local Guardian's Address", blank=True)),
                ('local_guardian_contact_no', models.CharField(max_length=12, verbose_name=b"Local Guardian's Contact No", blank=True)),
                ('category', models.CharField(blank=True, max_length=3, choices=[(b'GEN', b'General'), (b'SC', b'Scheduled Caste'), (b'ST', b'Scheduled Tribe'), (b'OBC', b'Other Backward Classes')])),
                ('nationality', models.CharField(max_length=100, blank=True)),
                ('marital_status', models.CharField(blank=True, max_length=3, verbose_name=b'Marital Status', choices=[(b'SIN', b'Single'), (b'MAR', b'Married')])),
                ('blood_group', models.CharField(blank=True, max_length=3, verbose_name=b'Blood Group', choices=[(b'O+', b'O+'), (b'O-', b'O-'), (b'AB+', b'AB+'), (b'AB-', b'AB-'), (b'A+', b'A+'), (b'A-', b'A-'), (b'B+', b'B+'), (b'B-', b'B-')])),
                ('physically_disabled', models.BooleanField(default=False, verbose_name=b'Physically Disabled')),
                ('fulltime', models.BooleanField(default=False)),
                ('resident', models.BooleanField(default=True)),
                ('license_no', models.CharField(max_length=100, verbose_name=b'License No', blank=True)),
                ('studentalumni', models.OneToOneField(primary_key=True, serialize=False, to='nucleus.StudentAlumni')),
            ],
            options={
                'verbose_name': 'Student Information (Alumni)',
                'verbose_name_plural': 'Students Information (Alumni)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WebmailAccount',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('webmail_id', models.CharField(max_length=15, serialize=False, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='studentalumni',
            name='branch',
            field=models.ForeignKey(to='nucleus.Branch'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='branch',
            field=models.ForeignKey(to='nucleus.Branch'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='registeredcoursechangealumni',
            name='studentalumni',
            field=models.ForeignKey(to='nucleus.StudentAlumni'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='registeredcoursechange',
            name='student',
            field=models.ForeignKey(to='nucleus.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='owner',
            name='account',
            field=models.ForeignKey(related_name=b'account_owners', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='owner',
            name='user',
            field=models.ForeignKey(related_name=b'user_owners', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='owner',
            unique_together=set([('account', 'user')]),
        ),
        migrations.AddField(
            model_name='introad',
            name='visited_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='from_user',
            field=models.ForeignKey(related_name=b'friendrequests_to', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='to_user',
            field=models.ForeignKey(related_name=b'friendrequests_from', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='friendrequest',
            unique_together=set([('from_user', 'to_user')]),
        ),
        migrations.AddField(
            model_name='connection',
            name='from_user',
            field=models.ForeignKey(related_name=b'from_people', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='connection',
            name='to_user',
            field=models.ForeignKey(related_name=b'to_people', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='batch',
            name='course',
            field=models.ForeignKey(to='nucleus.Course'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='batch',
            name='faculties',
            field=models.ManyToManyField(to='nucleus.Faculty', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='batch',
            name='students',
            field=models.ManyToManyField(to='nucleus.Student', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alumni',
            name='branch',
            field=models.ForeignKey(to='nucleus.Branch'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='connections',
            field=models.ManyToManyField(related_name=b'related_to+', null=True, through='nucleus.Connection', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='StudentUser',
            fields=[
            ],
            options={
                'verbose_name': 'Student User (Dummy)',
                'db_table': 'nucleus_student',
                'managed': False,
                'verbose_name_plural': 'Student Users (Dummy)',
            },
            bases=('nucleus.user', models.Model),
        ),
        migrations.CreateModel(
            name='StudentUserInfo',
            fields=[
            ],
            options={
                'verbose_name': 'Student User Information (Dummy)',
                'db_table': 'nucleus_studentinfo',
                'managed': False,
                'verbose_name_plural': 'Students User Information (Dummy)',
            },
            bases=('nucleus.studentuser', models.Model),
        ),
    ]
