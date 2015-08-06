from nucleus.models import *
from placement.models import *

from upload_xls import ExcelParser
def previous_sem(curr_sem):
  ''' curr_sem = "UG20" -> previous_sem = "UG11" '''
  try:
    disp = curr_sem[:2]
    if disp not in ["UG","PG"]:
        disp = "PHD"
    current_sem_code = curr_sem[-2:]
    current_sem_code_year = current_sem_code[0]
    current_sem_code_sem = current_sem_code[1]
    try:
      if current_sem_code_sem == "1":
        prev_sem_code_sem = "0"
        prev_sem_code_year = current_sem_code_year
      else:
        prev_sem_code_year = str(int(current_sem_code_year)-1)
        prev_sem_code_sem = "1"
      if prev_sem_code_year == "0":
        return ""
      return disp+prev_sem_code_year+prev_sem_code_sem
    except ValueError:
      return curr_sem
  except:
    if curr_sem == "":
      return curr_sem
    if curr_sem == "0":
      return curr_sem

rows = ExcelParser('SGPA_PG.xlsx')

failed = []
for l in rows:
  try:
    student = Student.objects.get(user__username=l['roll'])
  except Student.DoesNotExist:
    failed.append(l)
    continue
#import ipdb; ipdb.set_trace();
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
