# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '0006_auto_20150417_0353'),
        ('regol', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('semester', models.CharField(max_length=5)),
                ('grade', models.CharField(max_length=2)),
                ('course', models.ForeignKey(related_name=b'Grade_course', to='regol.CourseDetails')),
                ('person', models.ForeignKey(to='nucleus.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('data', models.FileField(upload_to=b'grades/')),
                ('semester', models.CharField(max_length=5, choices=[(b'UG10', b'UG(I Year I Semester)'), (b'UG11', b'UG(I Year II Semester)'), (b'UG20', b'UG(II Year I Semester)'), (b'UG21', b'UG(II Year II Semester)'), (b'UG30', b'UG(III Year I Semester)'), (b'UG31', b'UG(III Year II Semester)'), (b'UG40', b'UG(IV Year I Semester)'), (b'UG41', b'UG(IV Year II Semester)'), (b'UG50', b'UG(V Year I Semester)'), (b'UG51', b'UG(V Year II Semester)'), (b'ST1', b'Summer Term(I Year)'), (b'ST2', b'Summer Term(II Year)'), (b'ST3', b'Summer Term(III Year)'), (b'ST4', b'Summer Term(IV Year)'), (b'PG10', b'PG(I Year I Semester)'), (b'PG11', b'PG(I Year II Semester)'), (b'PG20', b'PG(II Year I Semester)'), (b'PG21', b'PG(II Year II Semester)'), (b'PG30', b'PG(III Year I Semester)'), (b'PG31', b'PG(III Year II Semester)'), (b'PHD10', b'PHD(I Year I Semester)'), (b'PHD11', b'PHD(I Year II Semester)'), (b'PHD20', b'PHD(II Year I Semester)'), (b'PHD21', b'PHD(II Year II Semester)'), (b'PHD30', b'PHD(III Year I Semester)'), (b'PHD31', b'PHD(III Year II Semester)'), (b'PHD40', b'PHD(IV Year I Semester)'), (b'PHD41', b'PHD(IV Year II Semester)'), (b'PHD50', b'PHD(V Year I Semester)'), (b'PHD51', b'PHD(V Year II Semester)'), (b'PHD60', b'PHD(VI Year I Semester)'), (b'PHD61', b'PHD(VI Year II Semester)'), (b'PHD70', b'PHD(VII Year I Semester)'), (b'PHD71', b'PHD(VII Year II Semester)'), (b'PHD80', b'PHD(VIII Year I Semester)'), (b'PHD81', b'PHD(VIII Year II Semester)'), (b'PHD90', b'PHD(IX Year I Semester)'), (b'PHD91', b'PHD(IX Year II Semester)')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
