# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('nucleus', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrativeBackground',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('from_year', models.CharField(max_length=10)),
                ('to_year', models.CharField(max_length=10)),
                ('designation', models.CharField(max_length=100)),
                ('organisation', models.CharField(max_length=100)),
                ('at_level', models.CharField(max_length=10, choices=[(b'D', b'Departmental'), (b'C', b'Central'), (b'I', b'Institute')])),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BooksAuthored',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('faculty', models.ForeignKey(primary_key=True, serialize=False, to='nucleus.Faculty')),
                ('books', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Collaboration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('topic', models.TextField()),
                ('organisation', models.CharField(max_length=100)),
                ('level', models.CharField(max_length=10, choices=[(b'UG', b'Undergraduate'), (b'PG', b'Postgraduate'), (b'PHD', b'PhD'), (b'RP', b'Research Project')])),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
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
                ('subject', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=10, null=True, blank=True)),
                ('university', models.CharField(max_length=100)),
                ('degree', models.CharField(max_length=100)),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FacSpace',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('space', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Honors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('year', models.CharField(max_length=10, null=True, blank=True)),
                ('award', models.CharField(max_length=100)),
                ('institute', models.CharField(max_length=100)),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Interests',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('general_topic', models.CharField(max_length=100)),
                ('research_work_topic', models.CharField(max_length=100)),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invitations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('topic', models.TextField()),
                ('organisation', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=10, choices=[(b'I', b'Invitation'), (b'T', b'Talk'), (b'G', b'Guest Lecture')])),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('year', models.CharField(max_length=10, null=True, blank=True)),
                ('visibility', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('organisation', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Miscellaneous',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('particulars_of_course', models.TextField(null=True, blank=True)),
                ('innovation_in_teaching', models.TextField(null=True, blank=True)),
                ('instructional_tasks', models.TextField(null=True, blank=True)),
                ('process_development', models.TextField(null=True, blank=True)),
                ('extension_tasks', models.TextField(null=True, blank=True)),
                ('other_work', models.TextField(null=True, blank=True)),
                ('self_appraisal', models.TextField(null=True, blank=True)),
                ('comments', models.TextField(null=True, blank=True)),
                ('separate_summary', models.TextField(null=True, blank=True)),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MultiplePost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('post', models.TextField()),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrganisedConference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('conference_name', models.CharField(max_length=100)),
                ('sponsored_by', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=10, null=True, blank=True)),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParticipationInShorttermCourses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('course_name', models.CharField(max_length=100)),
                ('sponsored_by', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=10, null=True, blank=True)),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParticipationSeminar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=100)),
                ('sponsored_by', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=10, null=True, blank=True)),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhdSupervised',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('topic', models.CharField(max_length=100)),
                ('name_of_other_supervisor', models.CharField(max_length=100, null=True, blank=True)),
                ('registration_year', models.CharField(max_length=10, null=True, blank=True)),
                ('status_of_phd', models.CharField(max_length=10, choices=[(b'A', b'Awarded'), (b'O', b'Ongoing')])),
                ('phd_type', models.CharField(max_length=10, choices=[(b'FULL', b'Fulltime'), (b'PART', b'Parttime')])),
                ('scholar_name', models.CharField(max_length=100)),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProfessionalBackground',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('from_year', models.CharField(max_length=10)),
                ('to_year', models.CharField(max_length=10)),
                ('designation', models.CharField(max_length=100)),
                ('organisation', models.CharField(max_length=100)),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectAndThesisSupervision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('title_of_project', models.CharField(max_length=100)),
                ('names_of_students', models.TextField()),
                ('name_of_other_supervisor', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.TextField()),
                ('course', models.CharField(max_length=100)),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RefereedJournalPapers',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('faculty', models.ForeignKey(primary_key=True, serialize=False, to='nucleus.Faculty')),
                ('papers', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResearchScholarGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('scholar_name', models.CharField(max_length=100)),
                ('interest', models.CharField(max_length=100)),
                ('home_page', models.URLField(null=True, blank=True)),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
                ('faculty', models.ForeignKey(to='nucleus.Faculty')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpecialLecturesDelivered',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('date', models.CharField(max_length=10, null=True, blank=True)),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
                ('faculty', models.ForeignKey(to='nucleus.Faculty')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SponsoredResearchProjects',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('financial_outlay', models.CharField(max_length=100)),
                ('funding_agency', models.CharField(max_length=100)),
                ('period', models.CharField(max_length=100, null=True, blank=True)),
                ('other_investigating_officer', models.CharField(max_length=100, null=True, blank=True)),
                ('status_of_project', models.CharField(default=b'O', max_length=10, choices=[(b'C', b'Completed'), (b'O', b'Ongoing')])),
                ('type_of_project', models.CharField(default=b'S', max_length=10, choices=[(b'S', b'Sponsored'), (b'C', b'Consultancy')])),
                ('year', models.IntegerField(max_length=10, choices=[(1915, 1915), (1916, 1916), (1917, 1917), (1918, 1918), (1919, 1919), (1920, 1920), (1921, 1921), (1922, 1922), (1923, 1923), (1924, 1924), (1925, 1925), (1926, 1926), (1927, 1927), (1928, 1928), (1929, 1929), (1930, 1930), (1931, 1931), (1932, 1932), (1933, 1933), (1934, 1934), (1935, 1935), (1936, 1936), (1937, 1937), (1938, 1938), (1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)])),
                ('topic', models.CharField(max_length=100)),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
                ('faculty', models.ForeignKey(to='nucleus.Faculty')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeachingEngagement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('class_name', models.CharField(max_length=100, null=True, blank=True)),
                ('semester', models.CharField(default=b'S', max_length=10, choices=[(b'S', b'Spring'), (b'A', b'Autumn')])),
                ('course_code', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=100)),
                ('no_of_students', models.IntegerField()),
                ('lecture_hours', models.IntegerField()),
                ('practical_hours', models.IntegerField()),
                ('tutorial_hours', models.IntegerField()),
                ('visibility', models.BooleanField(default=True)),
                ('faculty', models.ForeignKey(to='nucleus.Faculty')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Visits',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('purpose_of_visit', models.TextField()),
                ('institute_visited', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=10, null=True, blank=True)),
                ('priority', models.IntegerField(max_length=10, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24)])),
                ('visibility', models.BooleanField(default=True)),
                ('faculty', models.ForeignKey(to='nucleus.Faculty')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='projectandthesissupervision',
            name='faculty',
            field=models.ForeignKey(to='nucleus.Faculty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='professionalbackground',
            name='faculty',
            field=models.ForeignKey(to='nucleus.Faculty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='phdsupervised',
            name='faculty',
            field=models.ForeignKey(to='nucleus.Faculty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='participationseminar',
            name='faculty',
            field=models.ForeignKey(to='nucleus.Faculty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='participationinshorttermcourses',
            name='faculty',
            field=models.ForeignKey(to='nucleus.Faculty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organisedconference',
            name='faculty',
            field=models.ForeignKey(to='nucleus.Faculty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplepost',
            name='faculty',
            field=models.ForeignKey(to='nucleus.Faculty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='miscellaneous',
            name='faculty',
            field=models.ForeignKey(to='nucleus.Faculty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='membership',
            name='faculty',
            field=models.ForeignKey(to='nucleus.Faculty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invitations',
            name='faculty',
            field=models.ForeignKey(to='nucleus.Faculty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='interests',
            name='faculty',
            field=models.ForeignKey(to='nucleus.Faculty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='honors',
            name='faculty',
            field=models.ForeignKey(to='nucleus.Faculty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='educationaldetails',
            name='faculty',
            field=models.ForeignKey(to='nucleus.Faculty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collaboration',
            name='faculty',
            field=models.ForeignKey(to='nucleus.Faculty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='administrativebackground',
            name='faculty',
            field=models.ForeignKey(to='nucleus.Faculty'),
            preserve_default=True,
        ),
    ]
