from nucleus.models import *
from placement.models import *
from placement.utils import previous_sem
from upload_xls import ExcelParser


# XXX Beware of the usage of ExcelParser from upload_xls file
# The keys in row might change , for ex - in case of UG upload,
# keys are different, and in case of PG, its different

rows = ExcelParser('UG-07.01.2016.xlsx','4 YEAR')
app = []
for l in rows:
  student = Student.objects.get(user__username=l['roll'])
  student.cgpa = l['cgpa']
  student.save()
  try:
    try:
      edu = EducationalDetails.objects.get(student=student,course=previous_sem(student.semester))
      edu.sgpa = l['sgpa']
      edu.cgpa = l['cgpa']
      print student
      edu.save()
    except EducationalDetails.DoesNotExist:
      print student
      edu = EducationalDetails.objects.create(student=student, course=previous_sem(student.semester), sgpa=l['sgpa'], cgpa=l['cgpa'], year=2015, institution="Indian Institute of Technology, Roorkee", discipline=student.branch.code)
      edu.save()
    except:
      edu_lst = EducationalDetails.objects.filter(student=student,course=previous_sem(student.semester))
      for edu in edu_lst:
        edu.sgpa = l['sgpa']
        edu.cgpa = l['cgpa']
        print student
        edu.save()
  except:
    app.append(student)

print app
