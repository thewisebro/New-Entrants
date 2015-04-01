from django.core.management.base import BaseCommand, CommandError

from nucleus.models import Student

class Command(BaseCommand):
   args = ''
   help = 'Corrects various data after data migration from old database'

   def handle(self, *args, **options):
     students = Student.objects.filter(passout_year=None)
     print "Total students:", len(students)
     for i, student in enumerate(students):
        if student.semester[:2] in ['UG', 'PG']:
          rest = student.semester[2:]
        if student.semester[:3] == 'PHD':
          rest = student.semester[3:]
        if len(rest) == 2:
          year = int(rest[0])
          sem = int(rest[1])
          if year > 0:
            student.semester_no = (year-1)*2 + sem + 1
            student.admission_semtype = 'S' if (
                student.semester_no % 2 == 0) else 'A'
            student.save()
            print i, student
