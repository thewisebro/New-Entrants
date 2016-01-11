from nucleus.models import *
from placement.models import *
from placement.utils import *
from upload_xls import ExcelParser

rows = ExcelParser('PG-07.01.2016.xlsx', 'Sheet1')

failed = []
for l in rows:
  try:
    student = Student.objects.get(user__username=l['roll'])
    student.cgpa = l['cgpa']
    student.save()
  except Student.DoesNotExist:
    failed.append(l)
    continue
  if int(l['sem_no'])==220:
    course='PG20'
    year = '2015'
  if int(l['sem_no'])==230:
    course='PG30'
    year='2015'
  try:
   edu = EducationalDetails.objects.get(student=student,course=course)
   edu.sgpa = l['sgpa']
   edu.cgpa = l['cgpa']
   print student
   edu.save()
  except EducationalDetails.DoesNotExist:
   edu = EducationalDetails.objects.create(student=student, course=course, sgpa=l['sgpa'], cgpa=l['cgpa'], year=year, institution="Indian Institute of Technology, Roorkee", discipline=student.branch.code)
   edu.save()
  except:
   edu_lst = EducationalDetails.objects.filter(student=student,course=course)
   for edu in edu_lst:
     edu.sgpa = l['sgpa']
     edu.cgpa = l['cgpa']
     print student
     edu.save()
print failed
