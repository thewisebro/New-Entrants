from nucleus.models import *
from placement.models import *
from placement.utils import *
from upload_xls import ExcelParser

rows = ExcelParser('SGPA_PG.xlsx')

failed = []
for l in rows:
  try:
    student = Student.objects.get(user__username=l['roll'])
  except Student.DoesNotExist:
    failed.append(l)
    continue
  if int(l['sem_no'])==0:
    course='PG10'
    year = '2014'
  if int(l['sem_no'])==1:
    course='PG11'
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

#print previous_sem("UG10")
#print previous_sem("UG11")
#print previous_sem("UG20")
#print previous_sem("UG21")
#print previous_sem("PG10")
#print previous_sem("PG20")
#print previous_sem("UG41")
#print previous_sem("PG11")
#print previous_sem("PG21")
#print previous_sem("PHD10")
#print previous_sem("PHD11")
#print previous_sem("PHD51")
#print previous_sem("")
#print previous_sem("0")
#print previous_sem("UG0")
#print previous_sem("PG0")
#print previous_sem("PHD0")
