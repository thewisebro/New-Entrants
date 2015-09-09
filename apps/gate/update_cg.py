from django.conf import settings
settings.configure()
from mcm.views import *

mcms = MCM.objects.all()
for mcm in mcms:
  person = mcm.student
  student_info = EducationalDetails.objects.get(student=person,course=get_prev_sem(person.semester))
  mcm.sgpa = student_info.sgpa
  mcm.cgpa = student_info.cgpa
  mcm.save() 
