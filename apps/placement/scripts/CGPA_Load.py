from nucleus.models import *
from placement.models import *
from placement.utils import previous_sem
from upload_xls import ExcelParser


# XXX Beware of the usage of ExcelParser from upload_xls file
# The keys in row might change , for ex - in case of UG upload,
# keys are different, and in case of PG, its different

rows = ExcelParser('CGPA_2015.xlsx')

for l in rows:
  student = Student.objects.get(user__username=l['roll'])
  try:
   edu = EducationalDetails.objects.get(student=student,course=previous_sem(student.semester))
   edu.sgpa = l['sgpa']
   edu.cgpa = l['cgpa']
   print student
   edu.save()
  except EducationalDetails.DoesNotExist:
   edu = EducationalDetails.objects.create(student=student, course=previous_sem(student.semester), sgpa=l['sgpa'], cgpa=l['cgpa'], year=2015, institution="Indian Institute of Technology, Roorkee", discipline=student.branch.code)
   edu.save()
  except:
   edu_lst = EducationalDetails.objects.filter(student=student,course=previous_sem(student.semester))
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
