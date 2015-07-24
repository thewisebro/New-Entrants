# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0005_auto_20150415_0412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phpsession',
            name='datetime_created',
        ),
        migrations.AlterField(
            model_name='alumni',
            name='pincode',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='branch',
            name='code',
            field=models.CharField(max_length=10, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='branch',
            name='degree',
            field=models.CharField(max_length=10, choices=[(b'B.Tech.', b'Bachelor of Technology'), (b'B.Arch.', b'Bachelor of Architecture'), (b'IDD', b'Integrated Dual Degree'), (b'M.Tech.', b'Master of Technology'), (b'IMT', b'Integrated Master of Technology'), (b'IMSc', b'Integrated Master of Science'), (b'M.Arch.', b'Master of Architecture'), (b'MURP', b'Master of Urban and Regional Planning'), (b'PGDip', b'Postgraduate Diploma Course'), (b'MBA', b'Master of Business Administration'), (b'MCA', b'Master of Computer Applications'), (b'MSc', b'Master of Sciences'), (b'PHD', b'Doctor of Philosophy')]),
        ),
        migrations.AlterField(
            model_name='branch',
            name='department',
            field=models.CharField(max_length=10, choices=[(b'AHEC', b'Alternate Hydro Energy Centre'), (b'ASED', b'Applied Science and Engineering Department'), (b'CNT', b'Centre for Nanotechnology'), (b'ARCD', b'Architecture and Planning Department'), (b'BTD', b'Biotechnology Department'), (b'CHED', b'Chemical Engineering Department'), (b'CDM', b'Centre of Excellence in Disaster Mitigation and Management'), (b'CYD', b'Chemistry Department'), (b'CED', b'Civil Engineering Department'), (b'CSED', b'Computer Science and Engineering Department'), (b'CT', b'Centre for Transportation Systems'), (b'EQD', b'Earthquake Department'), (b'ESD', b'Earth Sciences Department'), (b'EED', b'Electrical Engineering Department'), (b'ECED', b'Electronics and Communication Engineering Department'), (b'HSD', b'Humanities and Social Sciences Department'), (b'HYD', b'Hydrology Department'), (b'MSD', b'Management Studies Department'), (b'MAD', b'Mathematics Department'), (b'MIED', b'Mechanical and Industrial Engineering Department'), (b'MMED', b'Metallurgical and Materials Engineering Department'), (b'PTD', b'Paper Technology Department'), (b'PPED', b'Polymer and Process Engineering Department'), (b'PHD', b'Physics Department'), (b'WRDMD', b'Water Resources Development and Management Department'), (b'CDM', b'Centre for Disaster Mitigation'), (b'ICC', b'Institute Computer Centre'), (b'IIC', b'Institute Instrumentation Centre'), (b'QIP', b'Quality Improvement Programme')]),
        ),
        migrations.AlterField(
            model_name='branch',
            name='graduation',
            field=models.CharField(max_length=10, choices=[(b'UG', b'Under Graduate'), (b'PG', b'Post Graduate'), (b'PHD', b'PhD')]),
        ),
        migrations.AlterField(
            model_name='course',
            name='subject_area',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='date_of_joining',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='department',
            field=models.CharField(max_length=10, choices=[(b'AHEC', b'Alternate Hydro Energy Centre'), (b'ASED', b'Applied Science and Engineering Department'), (b'CNT', b'Centre for Nanotechnology'), (b'ARCD', b'Architecture and Planning Department'), (b'BTD', b'Biotechnology Department'), (b'CHED', b'Chemical Engineering Department'), (b'CDM', b'Centre of Excellence in Disaster Mitigation and Management'), (b'CYD', b'Chemistry Department'), (b'CED', b'Civil Engineering Department'), (b'CSED', b'Computer Science and Engineering Department'), (b'CT', b'Centre for Transportation Systems'), (b'EQD', b'Earthquake Department'), (b'ESD', b'Earth Sciences Department'), (b'EED', b'Electrical Engineering Department'), (b'ECED', b'Electronics and Communication Engineering Department'), (b'HSD', b'Humanities and Social Sciences Department'), (b'HYD', b'Hydrology Department'), (b'MSD', b'Management Studies Department'), (b'MAD', b'Mathematics Department'), (b'MIED', b'Mechanical and Industrial Engineering Department'), (b'MMED', b'Metallurgical and Materials Engineering Department'), (b'PTD', b'Paper Technology Department'), (b'PPED', b'Polymer and Process Engineering Department'), (b'PHD', b'Physics Department'), (b'WRDMD', b'Water Resources Development and Management Department'), (b'CDM', b'Centre for Disaster Mitigation'), (b'ICC', b'Institute Computer Centre'), (b'IIC', b'Institute Instrumentation Centre'), (b'QIP', b'Quality Improvement Programme')]),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='designation',
            field=models.CharField(max_length=10, choices=[(b'HOD', b'Head Of Department'), (b'HOC', b'Head Of Centre'), (b'EP', b'Emeritus Professor'), (b'GF', b'Guest Faculty'), (b'WS', b'Workshop Superintendent'), (b'AWS', b'Assistant Workshop Superintendent'), (b'RF', b'Retired Faculty'), (b'SP', b'System Programmer'), (b'PRO', b'Professor'), (b'LEC', b'Lecturar'), (b'VS', b'Visiting Scientist'), (b'VP', b'Visiting Professor'), (b'SO', b'Scientific Officer'), (b'AP', b'Assistant Professor'), (b'CSO', b'Chief Scientific Officer'), (b'CP', b'Chair Professor'), (b'SSO', b'Senior Scientific Officer'), (b'JP', b'Joint Professor'), (b'ASP', b'Associate Professor'), (b'EF', b'Ex Faculty'), (b'EMF', b'Emeritus Fellows'), (b'APC', b'Assistant Professor (Contract)')]),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='employee_code',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='registeredcourse',
            name='cleared_status',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='registeredcourse',
            name='subject_area',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='bhawan',
            field=models.CharField(default=None, max_length=10, null=True, blank=True, choices=[(b'AZB', b'Azad Bhawan'), (b'CTB', b'Cautley Bhawan'), (b'GNB', b'Ganga Bhawan'), (b'GVB', b'Govind Bhawan'), (b'JWB', b'Jawahar Bhawan'), (b'RKB', b'Radhakrishnan Bhawan'), (b'RJB', b'Rajendra Bhawan'), (b'RGB', b'Rajiv Bhawan'), (b'RVB', b'Ravindra Bhawan'), (b'MVB', b'Malviya Bhawan'), (b'SB', b'Sarojini Bhawan'), (b'KB', b'Kasturba Bhawan'), (b'IB', b' Indra Bhawan'), (b'DAY', b'Day Scholar'), (b'KIH', b'Khosla International House')]),
        ),
        migrations.AlterField(
            model_name='student',
            name='room_no',
            field=models.CharField(max_length=10, verbose_name=b'Room No', blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='semester',
            field=models.CharField(max_length=10, choices=[(b'UG0', b'UG Overall'), (b'DPLM', b'Diploma'), (b'PG0', b'PG Overall'), (b'10TH', b'Tenth'), (b'12TH', b'Twelfth'), (b'UG10', b'UG(I Year I Semester)'), (b'UG11', b'UG(I Year II Semester)'), (b'UG20', b'UG(II Year I Semester)'), (b'UG21', b'UG(II Year II Semester)'), (b'UG30', b'UG(III Year I Semester)'), (b'UG31', b'UG(III Year II Semester)'), (b'UG40', b'UG(IV Year I Semester)'), (b'UG41', b'UG(IV Year II Semester)'), (b'UG50', b'UG(V Year I Semester)'), (b'UG51', b'UG(V Year II Semester)'), (b'ST1', b'Summer Term(I Year)'), (b'ST2', b'Summer Term(II Year)'), (b'ST3', b'Summer Term(III Year)'), (b'ST4', b'Summer Term(IV Year)'), (b'PG10', b'PG(I Year I Semester)'), (b'PG11', b'PG(I Year II Semester)'), (b'PG20', b'PG(II Year I Semester)'), (b'PG21', b'PG(II Year II Semester)'), (b'PG30', b'PG(III Year I Semester)'), (b'PG31', b'PG(III Year II Semester)'), (b'PHD10', b'PHD(I Year I Semester)'), (b'PHD11', b'PHD(I Year II Semester)'), (b'PHD20', b'PHD(II Year I Semester)'), (b'PHD21', b'PHD(II Year II Semester)'), (b'PHD30', b'PHD(III Year I Semester)'), (b'PHD31', b'PHD(III Year II Semester)'), (b'PHD40', b'PHD(IV Year I Semester)'), (b'PHD41', b'PHD(IV Year II Semester)'), (b'PHD50', b'PHD(V Year I Semester)'), (b'PHD51', b'PHD(V Year II Semester)'), (b'PHD60', b'PHD(VI Year I Semester)'), (b'PHD61', b'PHD(VI Year II Semester)'), (b'PHD70', b'PHD(VII Year I Semester)'), (b'PHD71', b'PHD(VII Year II Semester)'), (b'PHD80', b'PHD(VIII Year I Semester)'), (b'PHD81', b'PHD(VIII Year II Semester)'), (b'PHD90', b'PHD(IX Year I Semester)'), (b'PHD91', b'PHD(IX Year II Semester)'), (b'PHD0', b'PHD Overall'), (b'UG00', b'UG(New Entrants)')]),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='pincode',
            field=models.CharField(max_length=10, blank=True),
        ),
    ]
